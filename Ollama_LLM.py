import streamlit as st
st.set_page_config(page_title="ChatSphere", layout="centered")

from langchain_core.prompts import ChatPromptTemplate 
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import OllamaLLM
from datetime import datetime
import time
import base64
import speech_recognition as sr

st.title("💬 ChatSphere: Your AI-Powered Conversational Assistant")

st.sidebar.title("⚙️ Settings")
theme = st.sidebar.radio("Choose Theme:", ("🌑 Dark", "☀️ Light"))

if theme == "🌑 Dark":
    st.markdown("""
        <style>
        body {
            background: linear-gradient(to right, #232526, #414345);
            color: white;
        }
        .message-block {
            background-color: #2f2f2f;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        body {
            background: linear-gradient(to right, #fdfbfb, #ebedee);
        }
        .message-block {
            background-color: #e0e0e0;
            color: #000;
        }
        </style>
    """, unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "user_input" not in st.session_state:
    st.session_state.user_input = ""

llm = OllamaLLM(model="llama2")
output_parser = StrOutputParser()
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant. Your name is ChatSphere."),
    ("user", "User query: {query}")
])
chain = prompt | llm | output_parser

def format_message(sender, message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    icon = "🧑" if sender == "You" else "🤖"
    return f"""
    <div class="message-block" style="padding:12px; border-radius:10px; margin-bottom:15px;">
        <div class="sender">{icon} <strong>{sender}</strong> <span style='font-size: 0.8em; color: gray;'>[{timestamp}]</span></div>
        <div>{message}</div>
    </div>
    """

def listen_to_mic():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎙️ Listening... speak now!")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)  
        st.success("✅ Transcribed!")
        return text
    except Exception as e:
        st.error(f"Error: {e}")  
        return ""

def generate_response():
    user_input = st.session_state.user_input.strip()
    if user_input:
        with st.spinner("Generating response..."):
            try:
                response = chain.invoke({"query": user_input})

                replacements = {
                    "*smiles*": "😊",
                    "*smiling*": "😊",
                    "*smiling face*": "😊",
                    "*laughs*": "😂",
                    "*nods*": "👍",
                    "*sighs*": "😌",
                    "*adjusts glasses*": "🤖",
                    "*grin*": "😁",
                    "*bounces up and down excitedly*": "🕺",
                    "*smiling emoji*": "😊",
                    "*adjusts aviator sunglasses*": "😎",
                    "*winks*": "😉",

                }
                for pattern, emoji in replacements.items():
                    response = response.replace(pattern, emoji)

                st.session_state.messages.append(("You", user_input))
                st.session_state.messages.append(("ChatSphere", response))

            except Exception as e:
                st.session_state.messages.append(("ChatSphere", f"⚠️ Error: {e}"))

        st.session_state.user_input = ""

if st.sidebar.button("🗑️ Reset Chat"):
    st.session_state.messages = []

if st.sidebar.button("🎙️ Speak Query"):
    spoken_text = listen_to_mic()
    if spoken_text:
        st.session_state.user_input = spoken_text
        generate_response()

st.text_input("Please enter your queries...", key="user_input", on_change=generate_response)

st.markdown("---")

# ✅ Only one clean rendering of messages
for sender, message in st.session_state.messages:
    st.markdown(format_message(sender, message), unsafe_allow_html=True)

scroll_anchor = st.empty()
with scroll_anchor:
    st.markdown("<div id='scroll-to-bottom'></div>", unsafe_allow_html=True)
    st.markdown("""
        <script>
            var element = document.getElementById("scroll-to-bottom");
            if (element) element.scrollIntoView({behavior: "smooth"});
        </script>
    """, unsafe_allow_html=True)
