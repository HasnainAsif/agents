# HOW TO RUN THIS FILE:
# checkout terminal to /6_mcp/mcp_from_labs/ and run the command there.
# Use "uv run 4_lab1_investigator_agent.py" to run this file.

# I made a lot of tries to run this:
#   FileSystem MCP Serve didn't work on windows 
#   Playwright MCP Server worked and made 10 tries but unable to find anything.

import asyncio
from agents.mcp import MCPServerStdio
from agents import Agent, Runner, trace
import os
from dotenv import load_dotenv
load_dotenv() # Load environment variables from .env file

sandbox_path = os.path.abspath(os.path.join(os.getcwd(), '..', "sandbox"))
print("sandbox_path: ", sandbox_path)

async def main():
    # files_params = {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-filesystem", sandbox_path]} # For linux and Mac, use this command to run npx command
    # playwright_params = {"command": "npx","args": [ "@playwright/mcp@latest"]} # For linux and Mac, use this command to run npx command
    files_params = {"command": "cmd", "args": ["/c", "npx", "-y", "@modelcontextprotocol/server-filesystem", sandbox_path]} # for windows, use cmd to run npx command
    playwright_params = {"command": "cmd", "args": ["/c", "npx", "-y", "@playwright/mcp@latest"]} # for windows, use cmd to run npx command

    instructions = """
    You browse the internet to accomplish your instructions.
    You are highly capable at browsing the internet independently to accomplish your task, 
    including accepting all cookies and clicking 'not now' as
    appropriate to get to the content you need. If one website isn't fruitful, try another. 
    trying different options and sites as needed.
    But keep in mind, do not search web more than 3 times for a single task.
    When you need to write files, you do that inside the sandbox folder only.
    """


    async with MCPServerStdio(params=files_params, client_session_timeout_seconds=180) as mcp_server_files:
        async with MCPServerStdio(params=playwright_params, client_session_timeout_seconds=180) as mcp_server_browser:
            agent = Agent(
                name="investigator",
                instructions=instructions,
                model="gpt-4o-mini",
                mcp_servers=[mcp_server_files, mcp_server_browser]
                )
            with trace("investigate-ai-agents"):
                result = await Runner.run(agent, "Find AI Agents latest tools, technologies and courses from web with references and design a path to learn AI Agents within 6 months, then summarize it in markdown to learn_aiagents_new.md")
                # result = await Runner.run(agent, "open google.com and summarize homepage and write markdown in sandbox/homepage.md")
                print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
