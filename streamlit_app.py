import streamlit as st
import time
import streamlit.components.v1 as components

st.set_page_config(page_title="Livestock Health Chatbot", page_icon="🐄", layout="wide")

# Inject HTML/CSS/JS and Sound
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
#chat-footer {
  padding: 8px;
  border-top: 1px solid #ccc;
}
.minimized {
  height: 40px !important;
}
</style>

<!-- Sound Effects -->
<audio id="sendSound" src="https://www.soundjay.com/buttons/sounds/button-16.mp3" preload="auto"></audio>
<audio id="receiveSound" src="https://www.soundjay.com/button/beep-07.wav" preload="auto"></audio>

<script>
let widget = null;
let header = null;
let offsetX = 0, offsetY = 0;
let isDragging = false;

window.onload = () => {
  widget = document.getElementById("chat-widget");
  header = document.getElementById("chat-header");

  header.ondblclick = () => {
    widget.classList.toggle("minimized");
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
};

function playSendSound() {
  document.getElementById('sendSound').play();
}
function playReceiveSound() {
  document.getElementById('receiveSound').play();
}
</script>

<div id="chat-widget">
  <div id="chat-header">🐄 Livestock Health Chat</div>
  <div id="chat-body"><!-- Dynamic content injected by Streamlit --></div>
</div>
""", height=0)

# Session message state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Response generator
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

# Chat UI container
with st.container():
    st.markdown("""
    <style>
    .chat-box { position: fixed; bottom: 90px; right: 45px; width: 320px; max-height: 370px; overflow-y: auto; background: #f8f8f8; padding: 10px; border-radius: 10px; font-size: 14px; }
    .user { font-weight: bold; color: #0072C6; margin-bottom: 4px; }
    .bot { font-weight: normal; color: #111; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

    chat_container = st.empty()

    def display_messages():
        chat_html = '<div class="chat-box">'
        for msg in st.session_state.messages:
            role_class = "user" if msg["role"] == "user" else "bot"
            chat_html += f'<div class="{role_class}">{msg["content"]}</div>'
        chat_html += "</div>"
        chat_container.markdown(chat_html, unsafe_allow_html=True)

    display_messages()

    # User input
    prompt = st.chat_input("Ask about livestock health...")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        components.html("<script>playSendSound();</script>", height=0)  # 🔊 Play send sound
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
        components.html("<script>playReceiveSound();</script>", height=0)  # 🔊 Play receive sound
        thinking_placeholder.empty()
        display_messages()
