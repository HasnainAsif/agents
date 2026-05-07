# HOW TO RUN THIS FILE:
# checkout terminal to /6_mcp/mcp_from_labs/ and run the command there.
# Use "uv run 3_lab1_filesystem_mcp.py" to run this file.

import asyncio
from agents.mcp import MCPServerStdio
import os

sandbox_path = os.path.abspath(os.path.join(os.getcwd(), '..', "sandbox"))
print("sandbox_path: ", sandbox_path)

async def main():
    # files_params = {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-filesystem", sandbox_path]} # For linux and Mac, use this command to run npx command
    files_params = {"command": "cmd", "args": ["/c", "npx", "-y", "@modelcontextprotocol/server-filesystem", sandbox_path]} # for windows, use cmd to run npx command

    async with MCPServerStdio(
        params=files_params,
        client_session_timeout_seconds=60
    ) as server:

        filesystem_tools = await server.list_tools()
        # filesystem_tools = await server.session.list_tools()
        print(filesystem_tools)

if __name__ == "__main__":
    asyncio.run(main())
