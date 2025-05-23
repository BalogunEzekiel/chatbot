import streamlit as st
import time
import streamlit.components.v1 as components

st.set_page_config(page_title="Livestock Health Chatbot", page_icon="🐄", layout="wide")

# Inject CSS/HTML/JS for the widget
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
  z-index: 9999;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  resize: both;
}
#chat-header {
  background-color: #00a676;
  color: white;
  padding: 8px;
  text-align: center;
  font-weight: bold;
  cursor: move;
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
  <div id="chat-body"><!-- Filled by Streamlit --></div>
</div>
""", height=0)

# State management
if "messages" not in st.session_state:
    st.session_state.messages = []

# Response generator
def get_livestock_response(user_input):
    user_input_lower = user_input.lower()
    keywords = {
        "hi": "Hello there! How can I help you today?",
        "help": "Sure, I’m here to help! Can you tell me a bit more about what you need?",
        "assist": "Absolutely! Just let me know what you're looking for or need help with about animal care.",
        "new": "Welcome! 🎉 Would you like a quick tour of VetSmart app or ask me questions about livestock?",
        "exercise": "Regular movement is beneficial; ensure adequate pasture space.",
        "biosecurity": "Limit outside animal contact, quarantine new animals, and sanitize equipment.",
        "zoonotic": "Yes, such as brucellosis and Q fever; practice good hygiene.",
        "foot rot": "A bacterial infection causing lameness; prevent with dry conditions and hoof care.",
        "internal parasite": "Regular deworming and rotational grazing.",
        "common diseases": "Respiratory infections, parasitic infestations, and foot rot.",
        "ventilation": "Yes, proper ventilation reduces respiratory issues.",
        "bedding": "Regularly, at least once a week, to maintain cleanliness.",
        "floor": "Non-slip, easy-to-clean surfaces like packed dirt or rubber mats.",
        "space": "Cattle: ~20-50 sq. ft. indoors; Goats/Sheep: ~15-20 sq. ft.",
        "shelter": "Protection from extreme weather; well-ventilated barns or sheds.",
        "breeding": "Cattle: ~12 months; Goats/Sheep: 7-9 months.",
        "offspring": "Cattle: usually one; Goats/Sheep: one to three.",
        "heat": "Restlessness, vocalization and mounting behavior.",
        "gestation": "Cattle: ~283 days; Goats: ~150 days; Sheep: ~147 days.",
        "toxic": "Yes, plants like oleander, rhododendron and nightshade are toxic.",
        "water": "Cattle: 10-20 gallons; Goats/Sheep: 1-4 gallons.",
        "grazing together": "Yes, but monitor to prevent overgrazing and ensure balanced nutrition.",
        "diet": "Primarily forage-based, supplemented with grains as needed.",
        "mature": "Cattle: 1-2 years; Goats/Sheep: 6-12 months.",
        "live": "Cattle can live up to 20 years, goats and sheep around 10 to 12 years.",
        "fever": "Isolate the animal and consult a veterinarian.",
        "diarrhea": "Keep the animal hydrated and call a vet.",
        "not eating": "Watch for other signs and contact an expert.",
        "vaccination": "Ask a vet for a tailored vaccination schedule.",
        "bloat": "Bloat is life-threatening. Avoid risky feed and call your vet."
    }
    for key, val in keywords.items():
        if key in user_input_lower:
            return val
    return "Can you provide more information about your livestock’s symptoms or behavior?"

# Display chat messages
chat_container = st.container()
def display_chat():
    chat_html = '<div class="chat-box">'
    for m in st.session_state.messages:
        style = 'user' if m["role"] == "user" else "bot"
        chat_html += f'<div class="{style}">{m["content"]}</div>'
    chat_html += "</div>"
    chat_container.markdown(chat_html, unsafe_allow_html=True)

display_chat()

# Input box
user_input = st.chat_input("Ask about livestock health...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    components.html("<script>playSendSound();</script>", height=0)

    with st.spinner("Thinking..."):
        time.sleep(1.2)
        reply = get_livestock_response(user_input)

    st.session_state.messages.append({"role": "assistant", "content": reply})
    components.html("<script>playReceiveSound();</script>", height=0)
    display_chat()
