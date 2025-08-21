import os
import streamlit as st
import asyncio
import time
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

# Load env vars
load_dotenv()
# GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Function to run your agent with a given prompt
async def run_agent_async(user_prompt: str):
    client = MultiServerMCPClient(
        {
            "EducosysFileSystem": {
                "command": "python",
                "args": ["./filesystem_mcp.py"],
                "transport": "stdio",
            }
        }
    )
    tools = await client.get_tools()
    agent = create_react_agent("groq:llama-3.1-8b-instant", tools)

    response = await agent.ainvoke({
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a file management assistant. "
                    "Only use the provided tools. "
                    "If the user asks to delete a file, only call deleteFile, "
                    "do not recreate it."
                )
            },
            {"role": "user", "content": user_prompt}
        ]
    })
    return response["messages"][-1].content

# Wrapper to call async from Streamlit
def run_agent(user_prompt: str):
    return asyncio.run(run_agent_async(user_prompt))

# Streamlit UI
st.set_page_config(page_title="Groq Agent", page_icon="🤖", layout="centered")
st.title("💬 Work with file system like Magic!!")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm your File system assistant. What would you like me to do?"}
    ]

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Accept user input
if prompt := st.chat_input("Type your request..."):
    # Save and show user msg
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call your tool agent
    with st.chat_message("assistant"):
        message_placeholder = st.empty()

    # 🔹 Typing dots animation while waiting
    for i in range(6):  # ~3 seconds animation
        dots = "." * ((i % 3) + 1)
        message_placeholder.markdown(f"Thinking{dots}")
        time.sleep(0.5)

    # Now run the agent and replace with actual response
    try:
        result = run_agent(prompt)  # <-- your agent call here
    except Exception as e:
        result = f"⚠️ Error: {e}"

    message_placeholder.markdown(result)
    # Save assistant reply
    st.session_state.messages.append({"role": "assistant", "content": result})
