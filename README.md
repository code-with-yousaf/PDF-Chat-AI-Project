# 🌌 AI Assistant SaaS Dashboard

A beautiful, modern AI-powered chat assistant with PDF document analysis, web search, and multilingual support. Features a stunning deep space theme with glassmorphism design.

![AI Assistant Dashboard](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

## ✨ Features

- 🤖 **AI Chat Assistant** - Powered by Llama 3.2 via Ollama
- 📄 **PDF Document Analysis** - Upload and chat with your PDFs using RAG
- 🌐 **Web Search Integration** - Real-time search using DuckDuckGo
- 🎙️ **Voice Input** - Record voice messages
- 🔊 **Text-to-Speech** - AI voice responses
- 🌍 **Multilingual Support** - English, Urdu, Arabic, and more
- 📝 **Smart Notes** - Save and manage important conversations
- 🎨 **Beautiful UI** - Deep space theme with glassmorphism and animations

## 🚀 Live Demo

[Deploy on Streamlit Cloud](https://share.streamlit.io)

## 🛠️ Installation

### Prerequisites
- Python 3.11+
- Ollama installed locally with `llama3.2:3b` and `nomic-embed-text` models

### Setup

1. Clone the repository:
```bash
git clone https://github.com/mayanbuilds/PDF-Chat-AI-Dashboard.git
cd PDF-Chat-AI-Dashboard
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install Ollama models:
```bash
ollama pull llama3.2:3b
ollama pull nomic-embed-text
```

4. Run the app:
```bash
streamlit run app.py
```

## 📦 Dependencies

- Streamlit - Web framework
- LlamaIndex - RAG and document processing
- Ollama - Local LLM inference
- Edge-TTS - Text-to-speech
- DuckDuckGo-Search - Web search
- Audio Recorder - Voice input

## 🎨 UI Design

Inspired by modern SaaS dashboards with:
- Deep space background (#08090e)
- 60 animated twinkling stars
- Glassmorphism cards with backdrop blur
- Glowing logo with float animation
- Central light beam effect
- Responsive icon sidebar navigation

## 📝 Usage

1. **Chat Mode** - Ask anything, get AI-powered responses
2. **Sources** - Upload PDF documents for analysis
3. **Studio** - Access AI tools and features
4. **Settings** - Customize language, TTS, and preferences

## 🌐 Deployment

### Streamlit Cloud
1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Select this repository
5. Deploy!

**Note:** Ollama models won't work on Streamlit Cloud (requires local installation). Consider using OpenAI API for cloud deployment.

## 👨‍💻 Author

**Mayan Builds**
- GitHub: [@mayanbuilds](https://github.com/mayanbuilds)
- Email: yousafkhan122666@gmail.com

## 📄 License

MIT License - feel free to use this project!

## 🙏 Acknowledgments

- UI Design inspired by Behance AI Assistant SaaS concepts
- Powered by Llama 3.2 and Ollama
- Built with ❤️ using Streamlit

---

⭐ Star this repo if you find it useful!
