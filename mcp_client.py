import anyio

from mcp import Client


async def main():

    async with Client("http://127.0.0.1:8000/mcp") as client:

        print("Connected to:", client.server_info.name)
        print()

        response = await client.list_tools()

        print("Available tools:")

        for tool in response.tools:
            print(f"- {tool.name}: {tool.description}")

        print("\nCalling create_user...")

        result = await client.call_tool(
            "create_user",
            {
                "name": "Ahmed",
                "email": "ahad@gmail.com"
            }
        )

        print("\nTool result:")
        print(result)


if __name__ == "__main__":
    anyio.run(main)