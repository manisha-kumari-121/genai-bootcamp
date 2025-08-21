import os
import time
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Streamlit page config
st.set_page_config(page_title="Groq Chat", page_icon="🤖", layout="centered")
st.title("💬 Chat with Groq")
st.caption("Using Groq chat completion with streaming responses")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "assistant", "content": "Hello there! Ready to chat?"}
    ]

# Display chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# When user inputs a message
if prompt := st.chat_input("Type your message..."):
    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepare to stream assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        try:
            # Call Groq API with streaming enabled
            stream = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=st.session_state.messages,
                stream=True
            )

            # Stream and display content
            for chunk in stream:
                # Expect delta.content based on SDK spec
                content = None
                if hasattr(chunk.choices[0], "delta") and chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content

                if content:
                    full_response += content
                    message_placeholder.markdown(full_response + "▌")

            message_placeholder.markdown(full_response)

        except Exception as e:
            # Display error in chat bubble
            error_msg = f"Error contacting Groq API: {e}"
            message_placeholder.markdown(error_msg)
            full_response = error_msg

    # Save the assistant's response to history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
