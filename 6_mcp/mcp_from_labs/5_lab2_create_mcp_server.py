# HOW TO RUN THIS FILE:
# checkout terminal to /6_mcp/mcp_from_labs/ and run the command there.
# Use "uv run 5_lab2_create_mcp_server.py" to run this file.

import sys, os
from pathlib import Path

from gradio import context

# accounts_client.py and accounts_server.py live in the parent 6_mcp/ directory
_parent = Path(__file__).parent.parent
sys.path.insert(0, str(_parent))
os.chdir(_parent)  # so accounts_client spawns accounts_server.py from the right directory

import asyncio
from agents.mcp import MCPServerStdio
from agents import Agent, Runner, trace
from IPython.display import display, Markdown
from dotenv import load_dotenv

from accounts_client import get_accounts_tools_openai, read_accounts_resource, list_accounts_tools

load_dotenv(override=True)

async def main():
    ### Run MCP Server and list tools
    # params = {"command": "uv", "args": ["run", "../accounts_server.py"]}
    # async with MCPServerStdio(params=params, client_session_timeout_seconds=30) as mcp_server:
    #     mcp_tools = await mcp_server.list_tools()
    #     print("MCP Tools:", mcp_tools)

    #     print("-" * 50)

    #     instructions = "You are able to manage an account for a client, and answer questions about the account."
    #     request = "My name is Hasnain and my account is under the name Hasnain. What's my balance and my holdings?"
    #     model = "gpt-4o-mini"

    #     agent = Agent(name="account_manager", instructions=instructions, model=model, mcp_servers=[mcp_server])
    #     with trace("account_manager"):
    #         result = await Runner.run(agent, request)
    #     print("FINAL OUTPUT: ", result.final_output)

    ### Using the client to list tools and call them, and read resources
    # mcp_tools = await list_accounts_tools()
    # print("MCP Tools:")
    # print(mcp_tools)
    # print("-" * 50)
    # openai_tools = await get_accounts_tools_openai()
    # print("OpenAI Tools:")
    # print(openai_tools)
    # print("-" * 50)

    # instructions = "You are able to manage an account for a client, and answer questions about the account."
    # model = "gpt-4o-mini"
    # request = "My name is Hasnain and my account is under the name Hasnain. What's my balance?"

    # with trace("account_mcp_client"):
    #     agent = Agent(name="account_manager", instructions=instructions, model=model, tools=openai_tools)
    #     result = await Runner.run(agent, request)
    #     print(result.final_output)

    ### Reading resources directly using the client
    context = await read_accounts_resource("Hasnain")
    print(context)


if __name__ == "__main__":
    asyncio.run(main())