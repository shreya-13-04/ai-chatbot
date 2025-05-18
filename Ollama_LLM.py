import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.llms import HuggingFaceHub
from datetime import datetime

# Optional mic support
try:
    import speech_recognition as sr
    mic_available = True
except ModuleNotFoundError:
    mic_available = False

# --- Page Config ---
st.set_page_config(page_title="ChatSphere", layout="centered")

# --- Title & Sidebar ---
st.title("💬 ChatSphere: Your AI-Powered Conversational Assistant")
st.sidebar.title("⚙️ Settings")
theme = st.sidebar.radio("Choose Theme:", ("🌑 Dark", "☀️ Light"))

# --- Theme CSS ---
if theme == "🌑 Dark":
    st.markdown("""
        <style>
        body, .stApp {
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
        body, .stApp {
            background: linear-gradient(to right, #fdfbfb, #ebedee);
        }
        .message-block {
            background-color: #e0e0e0;
            color: black;
        }
        </style>
    """, unsafe_allow_html=True)

# --- Session State ---
if "messages" not in st.session_state:
    st.session_state.messages = []

if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# --- HuggingFace LLM ---
HUGGINGFACEHUB_API_TOKEN = st.secrets["huggingface_api_key"]
llm = HuggingFaceHub(
    repo_id="bigscience/bloom-560m",
    huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN,
    model_kwargs={"temperature": 0.5, "max_length": 256}
)
output_parser = StrOutputParser()
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant. Your name is ChatSphere."),
    ("user", "User query: {query}")
])
chain = prompt | llm | output_parser

# --- Format Message Block ---
def format_message(sender, message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    icon = "🧑" if sender == "You" else "🤖"
    return f"""
    <div class="message-block" style="padding:12px; border-radius:10px; margin-bottom:15px;">
        <div class="sender">{icon} <strong>{sender}</strong> <span style='font-size: 0.8em; color: gray;'>[{timestamp}]</span></div>
        <div>{message}</div>
    </div>
    """

# --- Listen via Mic ---
def listen_to_mic():
    if not mic_available:
        st.warning("🎙️ Microphone support is not available.")
        return ""
    
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎙️ Listening... Speak now...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        st.success("✅ Transcribed successfully!")
        return text
    except Exception as e:
        st.error(f"Transcription failed: {e}")
        return ""

# --- Generate Response ---
def generate_response():
    user_input = st.session_state.user_input.strip()
    if user_input:
        with st.spinner("Generating response..."):
            try:
                response = chain.invoke({"query": user_input})

                replacements = {
                    "*smiles*": "😊", "*smiling*": "😊", "*laughs*": "😂", "*nods*": "👍",
                    "*sighs*": "😌", "*adjusts glasses*": "🤖", "*grin*": "😁",
                    "*bounces up and down excitedly*": "🕺", "*smiling emoji*": "😊",
                    "*adjusts aviator sunglasses*": "😎", "*winks*": "😉"
                }
                for pattern, emoji in replacements.items():
                    response = response.replace(pattern, emoji)

                st.session_state.messages.append(("You", user_input))
                st.session_state.messages.append(("ChatSphere", response))
            except Exception as e:
                st.session_state.messages.append(("ChatSphere", f"⚠️ Error: {e}"))

        st.session_state.user_input = ""

# --- Reset Chat ---
if st.sidebar.button("🗑️ Reset Chat"):
    st.session_state.messages = []

# --- Mic Button ---
if mic_available and st.sidebar.button("🎙️ Speak Query"):
    spoken_text = listen_to_mic()
    if spoken_text:
        st.session_state.user_input = spoken_text
        generate_response()

# --- Text Input ---
st.text_input("Please enter your queries...", key="user_input", on_change=generate_response)

# --- Show Messages ---
st.markdown("---")
for sender, message in st.session_state.messages:
    st.markdown(format_message(sender, message), unsafe_allow_html=True)

# --- Auto Scroll ---
scroll_anchor = st.empty()
with scroll_anchor:
    st.markdown("<div id='scroll-to-bottom'></div>", unsafe_allow_html=True)
    st.markdown("""
        <script>
            var element = document.getElementById("scroll-to-bottom");
            if (element) element.scrollIntoView({behavior: "smooth"});
        </script>
    """, unsafe_allow_html=True)
