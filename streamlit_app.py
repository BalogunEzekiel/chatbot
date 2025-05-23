import streamlit as st
from openai import OpenAI

# Title and description
st.set_page_config(page_title="Chatbot", page_icon="💬")
st.title("💬 Chatbot with GPT-3.5")
st.write(
    """
    Welcome to the Streamlit Chatbot powered by OpenAI's GPT-3.5-turbo.  
    - Enter your OpenAI API key to begin.  
    - Your conversation will appear below and persist during the session.
    """
)

# Input for OpenAI API key
openai_api_key = st.text_input("🔐 Enter your OpenAI API Key", type="password")

if not openai_api_key:
    st.info("Please add your OpenAI API key above to start chatting.", icon="🗝️")
else:
    # Create OpenAI client
    client = OpenAI(api_key=openai_api_key)

    # Initialize session state for chat messages
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display existing chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input
    if prompt := st.chat_input("Say something..."):
        # Show user's message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response with streaming
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""

            stream = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=st.session_state.messages,
                stream=True
            )

            for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    full_response += content
                    response_placeholder.markdown(full_response)

        # Save assistant response
        st.session_state.messages.append({"role": "assistant", "content": full_response})
