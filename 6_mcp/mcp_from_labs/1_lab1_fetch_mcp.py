# HOW TO RUN THIS FILE:
# checkout terminal to /6_mcp/mcp_from_labs/ and run the command there.
# Use "uv run 1_lab1_fetch_mcp.py" to run this file.

import asyncio
from agents.mcp import MCPServerStdio

async def main():
    fetch_params = {
        "command": "uvx",
        "args": ["mcp-server-fetch"]
    }

    async with MCPServerStdio(
        params=fetch_params,
        client_session_timeout_seconds=60
    ) as server:

        fetch_tools = await server.list_tools()
        # fetch_tools = await server.session.list_tools()
        print(fetch_tools)

if __name__ == "__main__":
    asyncio.run(main())