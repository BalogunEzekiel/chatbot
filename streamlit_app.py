import streamlit as st
import time
import streamlit.components.v1 as components

st.set_page_config(page_title="Livestock Health Chatbot", page_icon="🐄", layout="wide")

# CSS & JavaScript Chat Widget Injection
components.html("""
<style>
#chat-widget {
  position: fixed;
  bottom: 30px;
  right: 30px;
  width: 350px;
  height: 500px;
  background: white;
  border: 2px solid #ccc;
  border-radius: 12px;
  box-shadow: 0 8px 16px rgba(0,0,0,0.3);
  z-index: 9999;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
#chat-header {
  background-color: #00a676;
  color: white;
  padding: 10px;
  text-align: center;
  font-weight: bold;
}
#chat-body {
  flex: 1;
  padding: 10px;
  overflow-y: auto;
  display: flex;
  flex-direction: column-reverse;  /* Show latest message at bottom */
}
#chat-footer {
  border-top: 1px solid #ccc;
  padding: 10px;
  background: #f4f4f4;
}
.message-user {
  color: #0072C6;
  font-weight: bold;
  margin-bottom: 5px;
}
.message-bot {
  color: #000;
  margin-bottom: 10px;
}
</style>

<audio id="sendSound" src="https://www.soundjay.com/buttons/sounds/button-16.mp3" preload="auto"></audio>
<audio id="receiveSound" src="https://www.soundjay.com/button/beep-07.wav" preload="auto"></audio>

<script>
function playSendSound() {
  document.getElementById('sendSound').play();
}
function playReceiveSound() {
  document.getElementById('receiveSound').play();
}
</script>

<div id="chat-widget">
  <div id="chat-header">🐄 Livestock Health Chat</div>
  <div id="chat-body" id="streamlit-chat-target"></div>
  <div id="chat-footer">
    <p style='font-size: 13px; color: #666;'>Use the input below the widget to chat</p>
  </div>
</div>
""", height=0)

# Initialize message history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Response function
def get_livestock_response(user_input):
    user_input = user_input.lower()
    match_phrases = {
        "hi": "Hello there! How can I help you today?",
        "help": "Sure, I’m here to help! Can you tell me a bit more about what you need?",
        "assist": "Absolutely! Let me know your livestock concern.",
        "new": "Welcome! 🎉 Would you like a tour of VetSmart app or ask me questions?",
        "yes": "Alright!",
        "thanks": "You're welcome!",
        "bye": "Goodbye!",
        "no": "Okay.",
        "exercise": "Regular movement is good; ensure pasture space.",
        "social": "Yes, animals thrive in social groups.",
        "biosecurity": "Limit contact, isolate newcomers, clean equipment.",
        "zoonotic": "Yes. Example: Q fever. Hygiene is vital.",
        "foot rot": "Causes lameness. Use dry grounds and hoof care.",
        "internal parasite": "Deworm regularly and rotate pasture.",
        "common diseases": "Respiratory, foot rot, parasites.",
        "ventilation": "Essential for reducing respiratory illness.",
        "bedding": "Change weekly or more if wet.",
        "floor": "Non-slip floors like dirt or rubber mats.",
        "space": "Cattle: 20-50 sq.ft; Goats/Sheep: 15-20 sq.ft",
        "shelter": "Ventilated barns/sheds protect from weather.",
        "breeding": "Cattle: ~12 months; Goats/Sheep: 7-9 months.",
        "offspring": "Cattle: 1; Goats/Sheep: 1-3 typically.",
        "heat": "Restless, mounting, vocalizing.",
        "gestation": "Cattle: 283d; Goats: 150d; Sheep: 147d.",
        "toxic": "Yes. Avoid oleander, nightshade, rhododendron.",
        "water": "Cattle: 10-20 gal; Goats/Sheep: 1-4 gal/day.",
        "grazing together": "Yes, monitor grazing and nutrition.",
        "diet": "Forage + grains as supplement.",
        "mature": "Cattle: 1-2 yrs; Goats/Sheep: 6-12 months.",
        "live": "Cattle: ~20 yrs; Goats/Sheep: ~10-12 yrs.",
        "fever": "Could mean infection. Isolate and call vet.",
        "diarrhea": "Hydrate. Likely parasites or poor diet.",
        "not eating": "May be ill. Monitor and call vet.",
        "vaccination": "Very important. Ask vet for schedule.",
        "bloat": "Life-threatening. Call vet immediately!"
    }
    for key in match_phrases:
        if key in user_input:
            return match_phrases[key]
    return "Can you tell me more about the livestock's behavior or symptoms?"

# Display messages
def display_messages():
    chat_html = '<div style="display:flex; flex-direction:column-reverse;">'
    for msg in reversed(st.session_state.messages):
        role_class = "message-user" if msg["role"] == "user" else "message-bot"
        chat_html += f'<div class="{role_class}">{msg["content"]}</div>'
    chat_html += "</div>"
    st.markdown(chat_html, unsafe_allow_html=True)

# Show chat in main Streamlit layout
with st.container():
    display_messages()
    user_input = st.chat_input("Ask about livestock health...")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        components.html("<script>playSendSound();</script>", height=0)
        time.sleep(1)
        reply = get_livestock_response(user_input)
        st.session_state.messages.append({"role": "assistant", "content": reply})
        components.html("<script>playReceiveSound();</script>", height=0)
        display_messages()
