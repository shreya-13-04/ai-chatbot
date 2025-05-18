# 💬 ChatSphere: Your Offline AI-Powered Conversational Assistant

ChatSphere is a privacy-first AI chatbot that runs **entirely on your local machine** using open-source large language models (LLMs) powered by [Ollama](https://ollama.com/). No cloud APIs, no internet required — just pure local inference with a sleek Streamlit interface.

---

## 🚀 Features

- 🤖 Chat with open-source LLMs (e.g., LLaMA 2, Mistral)
- 🎧 Voice input using your microphone (optional)
- 🌙 Light/Dark theme toggle
- 🧠 Local inference via Ollama (no API key needed)
- 📜 Memory of previous chat history during the session
- 🔄 Easy reset of chat
- ✅ Emoji replacements for expressive replies

---

## 🧠 Models You Can Use

You can use any Ollama-supported model, for example:

- `ollama run mistral`
- `ollama run llama2`
- `ollama run gemma`

✅ Just make sure the model is running when you launch the app.

---

## 📢 Voice Support

If you have a microphone and want to use voice input:

- Make sure the `speech_recognition` package is installed
- Use the 🎧 **Speak Query** button in the sidebar

> ⚠️ Note: Microphone input may not work in cloud-hosted environments.

---

## 📌 Notes

- 💡 This chatbot does **not require an API key** if you're using Ollama.
- 🌐 This app is meant to run **locally only** and is **not deployed** to Streamlit Cloud.
- 🔒 All conversations remain on your device — perfect for privacy-focused applications.

---

## 🤝 Contributions

Contributions are welcome! Feel free to:

- Suggest improvements
- Add support for more models
- Improve UI or voice features

---

## 🛠️ Installation Guide

### 1. Install Ollama

> 📌 Ollama is a lightweight local LLM runner. Supports models like `llama2`, `mistral`, and more.

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

## 🛠️ Requirements

Install Python packages:
```bash
pip install -r requirements.txt
```
Run the app:
```bash
python -m streamlit run Ollama_LLM.py
```
> 🗣️ Visit the localhost in your browser to chat!
