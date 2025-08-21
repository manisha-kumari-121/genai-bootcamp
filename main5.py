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
            "EducosysFileSystem": {
               "command": "python",
               "args": [
                   "./filesystem_mcp.py"
               ],
               "transport":"stdio"
           }

        }
       
      

   )
   tools = await client.get_tools()
   agent = create_react_agent("groq:llama-3.1-8b-instant", tools)

   response = await agent.ainvoke({  "messages": ("If the file 'test.txt' exists in the current directory, delete it. Do not create it.")
        
    })
   print(response["messages"][-1].content)


if __name__ == "__main__":
   asyncio.run(run_agent())