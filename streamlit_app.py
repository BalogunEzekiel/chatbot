import streamlit as st
# from openai import OpenAI  # Commented out OpenAI integration

# Title and description
st.set_page_config(page_title="Livestock Health Chatbot", page_icon="🐄")
st.title("🐄 Livestock Health Chatbot")
st.write(
    """
    Welcome to the Livestock Health Chatbot!  
    - Ask questions related to livestock health and care.  
    - Responses are generated using predefined logic based on your input.
    """
)

# Optional API Key Input (Disabled)
# openai_api_key = st.text_input("🔐 Enter your OpenAI API Key", type="password")

# Initialize session state for chat messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display existing chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Define response logic
def get_livestock_response(user_input):
    user_input_lower = user_input.lower()
    if "fever" in user_input_lower:
        return "A fever in livestock can indicate an infection. You should isolate the animal and contact a veterinarian."
    elif "diarrhea" in user_input_lower:
        return "Diarrhea can be caused by parasites or diet issues. Ensure the animal stays hydrated and consult a vet."
    elif "not eating" in user_input_lower or "loss of appetite" in user_input_lower:
        return "Loss of appetite may signal a digestive problem or illness. Observe for other symptoms and seek expert help."
    elif "vaccination" in user_input_lower:
        return "Vaccinations are vital to prevent diseases. Consult a vet for the proper vaccination schedule for your livestock."
    elif "bloat" in user_input_lower:
        return "Bloat is a serious condition. Avoid feeding high-risk foods and get veterinary attention immediately."
    else:
        return "Please provide more details about your livestock's condition or behavior so I can assist better."

# Chat input
if prompt := st.chat_input("Ask about livestock health..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response (OpenAI replaced with logic)
    response = get_livestock_response(prompt)

    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
