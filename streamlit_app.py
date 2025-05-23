import streamlit as st
import time
import streamlit.components.v1 as components

st.set_page_config(page_title="Livestock Health Chatbot", page_icon="🐄", layout="wide")

# Inject HTML/CSS/JS and Sound - Bottom Right Chat Widget
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
  resize: none;
}
#chat-header {
  background-color: #00a676;
  color: white;
  padding: 8px;
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
  <div id="chat-body"><!-- Streamlit content goes here --></div>
</div>
""", height=0)

# Session message state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Response generator
def get_livestock_response(user_input):
    user_input_lower = user_input.lower()
    if "hi" in user_input_lower or "hello" in user_input_lower:
        return "Hello there! How can I help you today?"
    elif "help" in user_input_lower:
        return "Sure, I’m here to help! Can you tell me a bit more about what you need?"
    elif "assist" in user_input_lower:
        return "Absolutely! Just let me know what you're looking for or need help with about animal care."
    elif "new" in user_input_lower:
        return "Welcome! 🎉 I'm glad you're here. Would you like a quick tour of VetSmart app or ask me questions about livestock."
    elif "yes" in user_input_lower or "alright" in user_input_lower:
        return "That's okay!."
    elif "thanks" in user_input_lower or "thank you" in user_input_lower:
        return "You're welcome!."
    elif "bye" in user_input_lower or "goodbye" in user_input_lower:
        return "Goodbye!."
    elif "no" in user_input_lower or "ok" in user_input_lower or "okay" in user_input_lower:
        return "Alrigt."
    elif "exercise" in user_input_lower:
        return "Regular movement is beneficial; ensure adequate pasture space."
    elif "social" in user_input_lower:
        return "Yes, animals thrive in groups."
    elif "biosecurity" in user_input_lower:
        return "Limit outside animal contact, quarantine new animals, and sanitize equipment."
    elif "zoonotic" in user_input_lower:
        return "Yes, such as brucellosis and Q fever; practice good hygiene."
    elif "foot rot" in user_input_lower:
        return "A bacterial infection causing lameness; prevent with dry conditions and hoof care."
    elif "internal parasite" in user_input_lower:
        return "Regular deworming and rotational grazing."
    elif "common diseases" in user_input_lower:
        return "Respiratory infections, parasitic infestations, and foot rot."
    elif "ventilation" in user_input_lower:
        return "Yes, proper ventilation reduces respiratory issues."
    elif "bedding" in user_input_lower:
        return "Regularly, at least once a week, to maintain cleanliness."
    elif "floor" in user_input_lower:
        return "Non-slip, easy-to-clean surfaces like packed dirt or rubber mats."
    elif "space" in user_input_lower:
        return "Cattle: ~20-50 sq. ft. indoors; Goats/Sheep: ~15-20 sq. ft."
    elif "shelter" in user_input_lower:
        return "Protection from extreme weather; well-ventilated barns or sheds."
    elif "breeding" in user_input_lower:
        return "Cattle: ~12 months; Goats/Sheep: 7-9 months."
    elif "offspring" in user_input_lower:
        return "Cattle: usually one; Goats/Sheep: one to three."
    elif "heat" in user_input_lower:
        return "Restlessness, vocalization and mounting behavior."
    elif "gestation" in user_input_lower:
        return "Cattle: ~283 days; Goats: ~150 days; Sheep: ~147 days."
    elif "toxic" in user_input_lower:
        return "Yes, plants like oleander, rhododendron and certain types of nightshade are toxic."
    elif "water" in user_input_lower:
        return "Cattle: 10-20 gallons; Goats/Sheep: 1-4 gallons, depending on size and climate."
    elif "grazing together" in user_input_lower:
        return "Yes, but monitor to prevent overgrazing and ensure balanced nutrition."
    elif "diet" in user_input_lower:
        return "Primarily forage-based, supplemented with grains as needed."
    elif "mature" in user_input_lower:
        return "Cattle: 1-2 years; Goats: 6-12 months; Sheep: 6-12 months."
    elif "live" in user_input_lower:
        return "Cattle can live up to 20 years, while goats and sheep often live around 10 to 12 years, depending on breed and care."
    elif "fever" in user_input_lower:
        return "A fever in livestock can indicate an infection. Isolate the animal and consult a veterinarian."
    elif "diarrhea" in user_input_lower:
        return "Diarrhea may result from parasites or poor diet. Keep the animal hydrated and call a vet."
    elif "not eating" in user_input_lower or "loss of appetite" in user_input_lower:
        return "A loss of appetite could mean illness. Watch for other signs and contact an expert."
    elif "vaccination" in user_input_lower:
        return "Vaccinations are essential. Ask a vet for a schedule tailored to your animals."
    elif "bloat" in user_input_lower:
        return "Bloat is serious and life-threatening. Avoid risky feed and act fast — call your vet."
    else:
        return "Can you provide more information about your livestock’s symptoms or behavior?"

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

    prompt = st.chat_input("Ask about livestock health...")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        components.html("<script>playSendSound();</script>", height=0)
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
        components.html("<script>playReceiveSound();</script>", height=0)
        thinking_placeholder.empty()
        display_messages()
