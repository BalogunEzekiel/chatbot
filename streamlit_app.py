import streamlit as st
import time
import streamlit.components.v1 as components

st.set_page_config(page_title="Livestock Health Chatbot", page_icon="🐄", layout="wide")

# Inject custom HTML, CSS, and JS
components.html("""
<style>
#chat-widget {
  position: fixed;
  bottom: 30px;
  right: 30px;
  width: 350px;
  height: 500px;
  background: #fff;
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
  padding: 8px;
  cursor: move;
  font-weight: bold;
  text-align: center;
  user-select: none;
}
#chat-body {
  flex-grow: 1;
  padding: 10px;
  overflow-y: auto;
  font-family: sans-serif;
  font-size: 14px;
}
#chat-messages {
  overflow-y: auto;
  height: 100%;
}
.minimized {
  height: 40px !important;
}
</style>
<script>
let widget = null;
let header = null;
let offsetX = 0, offsetY = 0;
let isDragging = false;

window.onload = () => {
  widget = document.getElementById("chat-widget");
  header = document.getElementById("chat-header");

  header.ondblclick = () => {
    if (widget.classList.contains("minimized")) {
      widget.classList.remove("minimized");
    } else {
      widget.classList.add("minimized");
    }
  };

  header.onmousedown = function(e) {
    isDragging = true;
    offsetX = e.clientX - widget.getBoundingClientRect().left;
    offsetY = e.clientY - widget.getBoundingClientRect().top;

    document.onmousemove = function(e) {
      if (isDragging) {
        widget.style.left = (e.clientX - offsetX) + "px";
        widget.style.top = (e.clientY - offsetY) + "px";
        widget.style.right = "auto";
        widget.style.bottom = "auto";
      }
    };

    document.onmouseup = function() {
      isDragging = false;
    };
  };

  // Auto-scroll on new messages
  const chatMessages = document.getElementById("chat-messages");
  const observer = new MutationObserver(() => {
    chatMessages.scrollTop = chatMessages.scrollHeight;
  });
  observer.observe(chatMessages, { childList: true, subtree: true });
};
</script>

<div id="chat-widget">
  <div id="chat-header">🐄 Livestock Health Chat</div>
  <div id="chat-body"><div id="chat-messages"></div></div>
</div>
""", height=0)

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Bot logic
def get_livestock_response(user_input):
    user_input_lower = user_input.lower()
    if "fever" in user_input_lower:
        return "🤒 A fever in livestock can indicate an infection. Isolate the animal and consult a veterinarian."
    elif "diarrhea" in user_input_lower:
        return "💧 Diarrhea may result from parasites or poor diet. Keep the animal hydrated and call a vet."
    elif "not eating" in user_input_lower or "loss of appetite" in user_input_lower:
        return "😟 A loss of appetite could mean illness. Watch for other signs and contact an expert."
    elif "vaccination" in user_input_lower:
        return "💉 Vaccinations are essential. Ask a vet for a schedule tailored to your animals."
    elif "bloat" in user_input_lower:
        return "⚠️ Bloat is serious and life-threatening. Avoid risky feed and act fast — call your vet."
    else:
        return "🤔 Can you provide more information about your livestock’s symptoms or behavior?"

# Chat UI styles and display logic
with st.container():
    st.markdown("""
    <style>
    .chat-box {
      position: fixed;
      bottom: 90px;
      right: 45px;
      width: 320px;
      max-height: 370px;
      overflow-y: auto;
      background: #f8f8f8;
      padding: 10px;
      border-radius: 10px;
      font-size: 14px;
    }
    .user { font-weight: bold; color: #0072C6; margin-bottom: 4px; }
    .bot { font-weight: normal; color: #111; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

    chat_container = st.empty()

    def display_messages():
        chat_html = '<div class="chat-box"><div id="chat-messages">'
        for msg in st.session_state.messages:
            role_class = "user" if msg["role"] == "user" else "bot"
            chat_html += f'<div class="{role_class}">{msg["content"]}</div>'
        chat_html += "</div></div>"
        chat_container.markdown(chat_html, unsafe_allow_html=True)

    display_messages()

    # User input
    prompt = st.chat_input("Ask about livestock health...")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        display_messages()

        thinking_placeholder = st.empty()
        thinking_placeholder.markdown("💭 Thinking...")
        time.sleep(1.5)

        response = get_livestock_response(prompt)
        slow_response = ""
        for char in response:
            slow_response += char
            thinking_placeholder.markdown(slow_response)
            time.sleep(0.03)

        st.session_state.messages.append({"role": "assistant", "content": response})
        thinking_placeholder.empty()
        display_messages()
