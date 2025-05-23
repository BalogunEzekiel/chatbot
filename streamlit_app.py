import streamlit as st
import streamlit.components.v1 as components
import time

st.set_page_config(page_title="Livestock Health Chatbot", page_icon="🐄", layout="wide")

# CSS + widget HTML + JS for draggable, resizable chat widget with sounds
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
  white-space: pre-wrap;
}
#chat-footer {
  padding: 8px;
  border-top: 1px solid #ccc;
}
.minimized {
  height: 40px !important;
}
.user-message {
  text-align: right;
  margin: 5px;
  color: #004d40;
  font-weight: 600;
}
.bot-message {
  text-align: left;
  margin: 5px;
  color: #00695c;
  font-weight: 600;
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

function typeText(elementId, text, speed=40) {
  let i = 0;
  const el = document.getElementById(elementId);
  el.textContent = '';
  function type() {
    if (i < text.length) {
      el.textContent += text.charAt(i);
      i++;
      setTimeout(type, speed);
    } else {
      playReceiveSound();
    }
  }
  type();
}
</script>

<div id="chat-widget">
  <div id="chat-header">🐄 Livestock Health Chat</div>
  <div id="chat-body"></div>
</div>
""", height=0)


# Chatbot response logic
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

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Input from user
user_input = st.text_input("Ask about livestock health...", key="input_box")

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    # Play send sound
    components.html("<script>playSendSound();</script>", height=0)

    # Get bot response
    with st.spinner("Thinking..."):
        time.sleep(1.2)
        bot_response = get_livestock_response(user_input)

    # Add bot response (do not display immediately; will be typed)
    st.session_state.messages.append({"role": "assistant", "content": bot_response})

# Prepare the chat HTML with user messages and placeholders for bot messages
chat_html = ""
typing_id_counter = 0
last_bot_id = None

for i, msg in enumerate(st.session_state.messages):
    if msg["role"] == "user":
        chat_html += f'<div class="user-message"><b>You:</b> {msg["content"]}</div>'
    else:
        # For the last bot message, we'll do typing animation, for previous, show full text
        if i == len(st.session_state.messages) - 1:
            typing_id = f"typing_{typing_id_counter}"
            last_bot_id = typing_id
            chat_html += f'<div class="bot-message"><b>Bot:</b> <span id="{typing_id}"></span></div>'
            typing_id_counter += 1
        else:
            chat_html += f'<div class="bot-message"><b>Bot:</b> {msg["content"]}</div>'

# Render chat inside chat-body
components.html(f"""
<div id="chat-body" style="height:100%; overflow-y:auto; font-family:sans-serif; font-size:14px;">
  {chat_html}
</div>

<script>
  // Scroll chat to bottom
  const chatBody = parent.document.getElementById("chat-body") || document.getElementById("chat-body");
  if(chatBody){ chatBody.scrollTop = chatBody.scrollHeight; }

  // Type text for last bot message
  const lastBotId = "{last_bot_id}";
  if(lastBotId) {{
    const text = `{st.session_state.messages[-1]["content"].replace("`", "\\`")}`;
    function typeText(id, txt, speed=40) {{
      let i = 0;
      const el = document.getElementById(id);
      if(!el) return;
      el.textContent = '';
      function type() {{
        if(i < txt.length) {{
          el.textContent += txt.charAt(i);
          i++;
          setTimeout(type, speed);
        }} else {{
          playReceiveSound();
        }}
      }}
      type();
    }}
    typeText(lastBotId, text);
  }}
</script>
""", height=520)
