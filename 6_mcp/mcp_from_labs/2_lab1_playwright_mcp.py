# HOW TO RUN THIS FILE:
# checkout terminal to /6_mcp/mcp_from_labs/ and run the command there.
# Use "uv run 2_lab1_playwright_mcp.py" to run this file.

import asyncio
from agents.mcp import MCPServerStdio

async def main():
    # playwright_params = {"command": "npx","args": [ "@playwright/mcp@latest"]} # For linux and Mac, use this command to run npx command
    playwright_params = {"command": "cmd", "args": ["/c", "npx", "@playwright/mcp@latest"]} # for windows, use cmd to run npx command

    async with MCPServerStdio(
        params=playwright_params,
        client_session_timeout_seconds=60
    ) as server:

        playwright_tools = await server.list_tools()
        # playwright_tools = await server.session.list_tools()
        print(playwright_tools)

if __name__ == "__main__":
    asyncio.run(main())