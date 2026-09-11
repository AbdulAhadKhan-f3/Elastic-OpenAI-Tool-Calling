import os
import json
import time
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
from mcp import Client

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROMPT_PATH = os.path.join(BASE_DIR, "SystemPrompt.md")

try:
    with open(PROMPT_PATH, "r", encoding="utf-8") as file:
        NEXUS_INSTRUCTIONS = file.read()
except FileNotFoundError:
    # Fallback or alert if the file is missing
    raise RuntimeError(f"Critical Error: System prompt file not found at {PROMPT_PATH}")


load_dotenv()

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MCP_SERVER_URL = "http://127.0.0.1:8000/mcp"
MAX_TURNS = 6  # safety cap so a stuck model can't loop forever and burn credits


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ---- startup ----
    global mcp_client, openai_tools_cache

    mcp_client = Client(MCP_SERVER_URL)
    await mcp_client.__aenter__()

    mcp_response = await mcp_client.list_tools()
    openai_tools_cache = [
        convert_mcp_tool_to_openai_tool(t) for t in mcp_response.tools
    ]

    print(f"[startup] Connected to MCP server, cached {len(openai_tools_cache)} tools")

    yield  # <-- app runs while suspended here

    # ---- shutdown ----
    if mcp_client is not None:
        await mcp_client.__aexit__(None, None, None)
        print("[shutdown] MCP client connection closed")


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


# -----------------------------------------
# Persistent MCP client + cached tool list
# -----------------------------------------
# These live for the lifetime of the FastAPI process instead of being
# recreated on every /api/chat call. Opening a connection and re-listing
# tools on every message was pure overhead, since the server and its
# tools don't change between requests.

mcp_client: Client | None = None
openai_tools_cache: list | None = None


def convert_mcp_tool_to_openai_tool(tool):
    return {
        "type": "function",
        "name": tool.name,
        "description": tool.description or "",
        "parameters": tool.input_schema,
    }


def extract_tool_result(mcp_result):
    """Pull the actual tool output from an MCP CallToolResult object."""
    if getattr(mcp_result, "structured_content", None):
        return mcp_result.structured_content

    if getattr(mcp_result, "content", None):
        parsed_blocks = []
        for block in mcp_result.content:
            text = getattr(block, "text", None)
            if text is None:
                continue
            try:
                parsed_blocks.append(json.loads(text))
            except (json.JSONDecodeError, TypeError):
                parsed_blocks.append(text)

        if len(parsed_blocks) == 1:
            return parsed_blocks[0]
        if len(parsed_blocks) > 1:
            return parsed_blocks
        return None

    return str(mcp_result)


async def run_agent(user_message: str):
    tool_calls_log = []

    response = openai_client.responses.create(
        model="gpt-5.6-luna",
        input=user_message,
        tools=openai_tools_cache,
        instructions=NEXUS_INSTRUCTIONS,
    )

    print(f"[run_agent] Initial model response: {response}")
    turns = 0

    while turns < MAX_TURNS:
        turns += 1
        tool_outputs = []
        
        for item in response.output:
            if item.type != "function_call":
                continue

            arguments = json.loads(item.arguments)
            start = time.perf_counter()

            try:
                mcp_result = await mcp_client.call_tool(item.name, arguments)
                elapsed_ms = round((time.perf_counter() - start) * 1000)
                clean_result = extract_tool_result(mcp_result)

                print(f"[run_agent] Tool '{item.name}' executed in {elapsed_ms} ms, result: {clean_result}")

                tool_calls_log.append({
                    "tool": item.name,
                    "arguments": arguments,
                    "result": clean_result,
                    "duration": elapsed_ms,
                    "status": "completed",
                })

                tool_outputs.append({
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": json.dumps(clean_result),
                })

            except Exception as e:
                elapsed_ms = round((time.perf_counter() - start) * 1000)

                tool_calls_log.append({
                    "tool": item.name,
                    "arguments": arguments,
                    "result": str(e),
                    "duration": elapsed_ms,
                    "status": "error",
                })

                tool_outputs.append({
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": f"Error: {e}",
                })

        if not tool_outputs:
            # No tool calls this round -> model is done, this is the final answer
            break

        response = openai_client.responses.create(
            model="gpt-5.6-luna",
            previous_response_id=response.id,
            input=tool_outputs,
            tools=openai_tools_cache,
        )

        print(f"[run_agent] Model response after tool calls: {response.output_text}")

    reply_text = response.output_text
    return reply_text, tool_calls_log


@app.post("/api/chat")
async def chat(req: ChatRequest):
    reply, tool_calls = await run_agent(req.message)
    return {"reply": reply, "tool_calls": tool_calls}


@app.get("/api/tools")
async def tools():
    return {"tools": openai_tools_cache or []}
    