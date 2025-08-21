import streamlit as st
import os
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
import asyncio

# Load environment variables
load_dotenv()

# Streamlit page setup
st.set_page_config(page_title="📧 Send Email via MCP", layout="centered")
st.title("📧 Send Email via LangGraph MCP Agent")

# Upload file
uploaded_file = st.file_uploader(
    "Upload a file to attach (optional)",
    type=["txt", "pdf", "csv", "docx", "xlsx"]
)

# Email details
to = st.text_input("Recipient Email")
subject = st.text_input("Subject")
body = st.text_area("Message Body")

# Save uploaded file temporarily
attachment_path = None
if uploaded_file is not None:
    os.makedirs("uploads", exist_ok=True)
    attachment_path = os.path.join("uploads", uploaded_file.name)
    with open(attachment_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

# Handle button click
if st.button("Send Email"):
    st.info("🚀 Sending email...")

    async def send_email_async():
        # 1️⃣ Initialize MCP client
        client = MultiServerMCPClient({
            "GmailSender": {
                "command": "python",
                "args": ["./gmail_mcp.py"],
                "transport": "stdio"
            }
        })

        # 2️⃣ Initialize Groq LLM
        llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            api_key=os.getenv("GROQ_API_KEY")
        )

        # 3️⃣ Get MCP tools
        tools = await client.get_tools()
        config = {"recursion_limit": 50}

        # 4️⃣ Create agent with recursion limit
        agent = create_react_agent(
            llm,
            tools
        )

        # 5️⃣ Prepare prompt
        prompt_text = f"Use the GmailSender tool to send an email to {to} with subject '{subject}' and body '{body}'."
        if attachment_path:
            prompt_text += f" Include this file: {attachment_path}."

        messages = [{"role": "user", "content": prompt_text}]
        print("Running agent with messages:", messages)

        # 6️⃣ Invoke agent
        result =  agent.invoke({"messages": messages},config=config)
        print("Agent response:", result)
        return result

    # Run the async function
    try:
        result = asyncio.run(send_email_async())
        st.success("✅ Email Sent Successfully!")
        st.write(result)
    except Exception as e:
        st.error(f"❌ Failed to send email: {e}")

    