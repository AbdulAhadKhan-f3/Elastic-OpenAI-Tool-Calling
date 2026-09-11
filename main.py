import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from tools.user_tools import (
    add_user,
    get_users,
    get_user,
    update_user,
    delete_user
)


load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


tools = [
    {
        "type": "function",
        "name": "add_user",
        "description": "Add a new user to the system.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The user's name"
                },
                "email": {
                    "type": "string",
                    "description": "The user's email address"
                }
            },
            "required": ["name", "email"],
            "additionalProperties": False
        },
        "strict": True
    },

    {
        "type": "function",
        "name": "get_users",
        "description": "Get all users from the system.",
        "parameters": {
            "type": "object",
            "properties": {},
            "additionalProperties": False
        },
        "strict": True
    },

    {
        "type": "function",
        "name": "get_user",
        "description": "Get a specific user by their ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "integer",
                    "description": "The ID of the user"
                }
            },
            "required": ["user_id"],
            "additionalProperties": False
        },
        "strict": True
    },

    {
        "type": "function",
        "name": "update_user",
        "description": "Update a user's name or email.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "integer",
                    "description": "The ID of the user"
                },
                "name": {
                    "type": ["string", "null"],
                    "description": "The new name"
                },
                "email": {
                    "type": ["string", "null"],
                    "description": "The new email"
                }
            },
            "required": ["user_id", "name", "email"],
            "additionalProperties": False
        },
        "strict": True
    },

    {
        "type": "function",
        "name": "delete_user",
        "description": "Delete a user by their ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "integer",
                    "description": "The ID of the user"
                }
            },
            "required": ["user_id"],
            "additionalProperties": False
        },
        "strict": True
    }
]


function_map = {
    "add_user": add_user,
    "get_users": get_users,
    "get_user": get_user,
    "update_user": update_user,
    "delete_user": delete_user
}


def run_tool(tool_name, arguments):
    function = function_map.get(tool_name)

    if function is None:
        return {
            "success": False,
            "error": f"Unknown tool: {tool_name}"
        }

    try:
        result = function(**arguments)

        return {
            "success": True,
            "result": result
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def main():

    user_input = input("You: ")

    response = client.responses.create(
        model="gpt-5",
        input=user_input,
        tools=tools
    )

    while True:

        tool_outputs = []

        for item in response.output:

            if item.type == "function_call":

                print(f"\n[Tool called: {item.name}]")

                arguments = json.loads(item.arguments)

                print(f"[Arguments: {arguments}]")

                result = run_tool(item.name, arguments)

                print(f"[Tool result: {result}]")

                tool_outputs.append({
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": json.dumps(result)
                })

        if not tool_outputs:
            break

        response = client.responses.create(
            model="gpt-5",
            previous_response_id=response.id,
            input=tool_outputs,
            tools=tools
        )

    print("\nAssistant:", response.output_text)


if __name__ == "__main__":
    main()