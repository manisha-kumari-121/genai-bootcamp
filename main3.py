from dotenv import load_dotenv
load_dotenv()
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
import os


GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


async def run_agent():
   client = MultiServerMCPClient(
       {
        #    "github": {
        #        "command": "npx",
        #        "args": [
        #            "-y",
        #            "@modelcontextprotocol/server-github"
        #        ],
        #        "env": {
        #            "GITHUB_PERSONAL_ACCESS_TOKEN": GITHUB_TOKEN
        #        },
        #        "transport": "stdio"
        #    }
         "gmail": {
                "command": "npx",
                "args": [
                    "-y",
                    "@modelcontextprotocol/server-gmail"
                ],
                "env": {
                    "GMAIL_USER": GMAIL_USER,
                    "GMAIL_PASS": GMAIL_PASS
                },
                "transport": "stdio"
            }
       }
   )
   tools = await client.get_tools()
   agent = create_react_agent("groq:llama-3.1-8b-instant", tools)
   
   gmail_response = await agent.ainvoke({
    "messages": (
        "Use ONLY the `send_mail` tool.\n"
        "{\n"
        f"  \"to\": \"rajatpatanjali@gmail.com\",\n"
        f"  \"subject\": \"Test Email from MCP\",\n"
        f"  \"body\": \"This is a test email sent using Gmail MCP agent.\"\n"
        "}"
        )
        })
        
        print("Gmail Response:", gmail_response["messages"][-1].content)

#print("Gmail Response:", gmail_response["messages"][-1].content)

#    response = await agent.ainvoke({  "messages": (
#      "Use ONLY the `push_files` tool.\n"
#         "Repo owner: manisha-kumari-121\n"
#         "Repo name: genai-bootcamp\n"
#         "Branch: main\n"
#         "Commit message: Added binary search code\n"
#         "The `files` field MUST be an array of objects, each with ONLY two fields: `path` and `content`.\n"
#         "For example:\n"
#         "{\n"
#         "  \"branch\": \"main\",\n"
#         "  \"files\": [\n"
#         "    {\"path\": \"binary_search.js\", \"content\": \"...javascript code...\"}\n"
#         "  ],\n"
#         "  \"message\": \"Added binary search code\",\n"
#         "  \"owner\": \"manisha-kumari-121\",\n"
#         "  \"repo\": \"genai-bootcamp\"\n"
#         "}\n"
#         "Now create `binary_search.js` containing a binary search implementation in JavaScript."
#     )})



if __name__ == "__main__":
   asyncio.run(run_agent())