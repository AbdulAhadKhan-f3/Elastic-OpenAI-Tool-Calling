import os
import json
import anyio

from dotenv import load_dotenv
from openai import OpenAI
from mcp import Client


load_dotenv()

openai_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def convert_mcp_tool_to_openai_tool(tool):
    return {
        "type": "function",
        "name": tool.name,
        "description": tool.description or "",
        "parameters": tool.input_schema,
    }


async def main():

    async with Client("http://127.0.0.1:8000/mcp") as mcp_client:

        # -----------------------------------------
        # 1. Discover MCP tools
        # -----------------------------------------

        mcp_response = await mcp_client.list_tools()

        openai_tools = [
            convert_mcp_tool_to_openai_tool(tool)
            for tool in mcp_response.tools
        ]

        # -----------------------------------------
        # 2. Send user request to OpenAI
        # -----------------------------------------

        user_request = (
            "Create a user named Bilal with email bilal@gmail.com."
        )

        response = openai_client.responses.create(
            model="gpt-5.6-luna",
            input=user_request,
            tools=openai_tools
        )

        # -----------------------------------------
        # 3. Look for tool calls
        # -----------------------------------------

        tool_outputs = []

        for item in response.output:

            if item.type == "function_call":

                print("\nOpenAI requested tool:")
                print("Tool:", item.name)
                print("Arguments:", item.arguments)

                arguments = json.loads(item.arguments)

                # -----------------------------------------
                # 4. Execute tool through MCP
                # -----------------------------------------

                mcp_result = await mcp_client.call_tool(
                    item.name,
                    arguments
                )

                print("\nMCP tool result:")
                print(mcp_result)

                # -----------------------------------------
                # 5. Send MCP result back to OpenAI
                # -----------------------------------------

                tool_outputs.append({
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": str(mcp_result)
                })

        # -----------------------------------------
        # 6. Ask OpenAI for the final response
        # -----------------------------------------

        if tool_outputs:

            final_response = openai_client.responses.create(
                model="gpt-5.6-luna",
                previous_response_id=response.id,
                input=tool_outputs
            )

            print("\nFinal answer:")
            print(final_response.output_text)


if __name__ == "__main__":
    anyio.run(main)