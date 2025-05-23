import streamlit as st
import streamlit.components.v1 as components
import time

def show_chatbot():
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
    };
    </script>
    <div id="chat-widget">
      <div id="chat-header">🐄 Livestock Health Chat</div>
      <div id="chat-body"><!-- Chat logic rendered via Streamlit below --></div>
    </div>
    """, height=0)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    def get_livestock_response(user_input):
        user_input_lower = user_input.lower()
        if "fever" in user_input_lower:
            return "🤒 A fever in livestock can indicate infection. Isolate the animal and call the vet."
        elif "diarrhea" in user_input_lower:
            return "💧 Diarrhea may result from parasites or poor diet. Hydration and vet visit needed."
        elif "not eating" in user_input_lower or "loss of appetite" in user_input_lower:
            return "😟 Could be illness or digestive trouble. Monitor and consult an expert."
        elif "vaccination" in user_input_lower:
            return "💉 Ask your vet for a vaccination schedule suited to your livestock."
        elif "bloat" in user_input_lower:
            return "⚠️ Bloat is an emergency. Avoid risky feeds and act fast."
        else:
            return "🤔 Please describe symptoms in more detail."

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
        display_messages()

        thinking_placeholder = st.empty()
        thinking_placeholder.markdown("💭 Thinking...")
        time.sleep(1.5)

        response = get_livestock_response(prompt)
        typed_response = ""
        for char in response:
            typed_response += char
            thinking_placeholder.markdown(typed_response)
            time.sleep(0.03)

        thinking_placeholder.empty()
        st.session_state.messages.append({"role": "assistant", "content": response})
        display_messages()
