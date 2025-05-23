import streamlit as st
import time
import streamlit.components.v1 as components

st.set_page_config(page_title="Livestock Health Chatbot", page_icon="🐄", layout="wide")

# Inject floating chatbox style and interactivity
components.html("""
<style>
#floating-chatbox {
  position: fixed;
  bottom: 30px;
  right: 30px;
  width: 350px;
  max-height: 500px;
  background: #ffffff;
  border: 2px solid #ccc;
  border-radius: 12px;
  box-shadow: 0 8px 16px rgba(0,0,0,0.3);
  overflow: hidden;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  resize: both;
}
#chat-header {
  background-color: #00a676;
  color: white;
  padding: 10px;
  cursor: move;
  font-weight: bold;
  text-align: center;
}
#chat-body {
  padding: 10px;
  overflow-y: auto;
  flex-grow: 1;
}
#chat-footer {
  padding: 10px;
  border-top: 1px solid #ccc;
}
</style>
<script>
let box = null;
window.onload = () => {
  box = document.getElementById("floating-chatbox");
  let header = document.getElementById("chat-header");
  let isDragging = false;
  let offsetX = 0;
  let offsetY = 0;

  header.onmousedown = function(e) {
    isDragging = true;
    offsetX = e.clientX - box.getBoundingClientRect().left;
    offsetY = e.clientY - box.getBoundingClientRect().top;
    document.onmousemove = function(e) {
      if (isDragging) {
        box.style.left = (e.clientX - offsetX) + "px";
        box.style.top = (e.clientY - offsetY) + "px";
        box.style.right = "auto";
        box.style.bottom = "auto";
      }
    };
    document.onmouseup = function() {
      isDragging = false;
    };
  };
};
</script>
""", height=0)

# Simulated chat logic
def get_livestock_response(user_input):
    user_input_lower = user_input.lower()
    if "fever" in user_input_lower:
        return "🤒 A fever in livestock can indicate an infection. You should isolate the animal and contact a veterinarian."
    elif "diarrhea" in user_input_lower:
        return "💧 Diarrhea can be caused by parasites or diet issues. Ensure the animal stays hydrated and consult a vet."
    elif "not eating" in user_input_lower or "loss of appetite" in user_input_lower:
        return "😟 Loss of appetite may signal a digestive problem or illness. Observe for other symptoms and use the Diagnosis tab to predict the disease."
    elif "vaccination" in user_input_lower:
        return "💉 Vaccinations are vital to prevent diseases. Consult a vet for the proper vaccination schedule for your livestock."
    elif "bloat" in user_input_lower:
        return "⚠️ Bloat is a serious condition. Avoid feeding high-risk foods and diagnose the disease based on symptoms observed."
    else:
        return "🤔 Please provide more details about your livestock's condition or behavior so I can assist better."

# Session for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Floating chat UI
with st.container():
    st.markdown('<div id="floating-chatbox">', unsafe_allow_html=True)
    st.markdown('<div id="chat-header">🐄 Livestock Chat</div>', unsafe_allow_html=True)
    st.markdown('<div id="chat-body">', unsafe_allow_html=True)

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    st.markdown('</div>', unsafe_allow_html=True)  # Close body

    prompt = st.chat_input("Ask about livestock health...")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Simulated thinking...
        thinking_message = "💭 Thinking..."
        with st.chat_message("assistant"):
            placeholder = st.empty()
            placeholder.markdown(thinking_message)
            time.sleep(1.2)
            response = get_livestock_response(prompt)
            placeholder.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})

    st.markdown('</div>', unsafe_allow_html=True)  # Close f
