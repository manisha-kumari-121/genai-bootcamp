from dotenv import load_dotenv
load_dotenv()
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
import os

# Load env vars
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASS = os.getenv("GMAIL_PASS")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")



async def run_agent():
    client = MultiServerMCPClient(
        {
            # "github": {
            #     "command": "npx",
            #     "args": [
            #         "-y",
            #         "@modelcontextprotocol/server-github"
            #     ],
            #     "env": {
            #         "GITHUB_PERSONAL_ACCESS_TOKEN": GITHUB_TOKEN
            #     },
            #     "transport": "stdio"
            # },
            "gmail": {
                "command": "npx",
                "args": [
                    "@gongrzhe/server-gmail-autoauth-mcp"
                ],
                "transport": "stdio",
            }
        }
    )

    tools = await client.get_tools()
    print("Available tools:", [t.name for t in tools])
    agent = create_react_agent("groq:llama-3.1-8b-instant", tools)

    auth_response = await agent.ainvoke({
    "messages": [
        {"role": "system", "content": "You have access to Gmail. Use ONLY the tools in the provided list. DO NOT make up APIs."},
        {"role": "user", "content": """Use the `send_email` tool to send an email to rajatpatanjali@gmail.com 
                with subject 'Test Email' and body 'This is a test email sent via MCP'."""}
    ],
    "tools": tools,
   })

    print("Gmail Response:", auth_response["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(run_agent())