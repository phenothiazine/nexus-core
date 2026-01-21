<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Gemini%20AI-Powered-4285F4?style=for-the-badge&logo=google&logoColor=white" alt="Gemini">
  <img src="https://img.shields.io/badge/ChromaDB-Vector%20Store-green?style=for-the-badge" alt="ChromaDB">
</p>

<p align="center">
  <a href="https://phenothiazine-nexus-core.streamlit.app/">
    <img src="https://img.shields.io/badge/🚀_Live_Demo-Try_Now-FF4B4B?style=for-the-badge" alt="Live Demo">
  </a>
</p>

<h1 align="center">⚫ Nexus-Core</h1>

<p align="center">
  <strong>An Intelligent Personal Knowledge Assistant with RAG-Powered Memory</strong>
</p>

<p align="center">
  <em>Think deeper. Remember everything. Answer smarter.</em>
</p>

---

## ✨ Features

### 🧠 **Intelligent Memory System (RAG)**
- **Persistent Knowledge Base**: Powered by ChromaDB vector database for semantic search
- **Document Ingestion**: Upload PDFs and TXT files to build your personal knowledge vault
- **Context-Aware Responses**: Automatically retrieves relevant information from memory

### 💬 **Advanced Chat Interface**
- **Multi-Session Management**: Create, switch, and manage multiple chat sessions
- **Smart Auto-Titling**: AI-generated titles based on conversation content
- **Pin & Organize**: Pin important conversations for quick access
- **Session Persistence**: All chats are preserved across sessions

### 🤔 **Chain of Thought Reasoning**
- **Transparent Thinking**: View the AI's reasoning process before answers
- **Structured Output**: Clear separation between thought process and final response
- **Referenced Memory**: See which memories were used to generate responses

### 🎨 **Modern UI/UX**
- **Minimalist Apple-like Design**: Clean, professional interface
- **Dark Mode Optimized**: Easy on the eyes for extended use
- **Responsive Layout**: Works seamlessly across different screen sizes

---

## 🏗️ Architecture

```
Nexus-Core/
├── main.py                 # Streamlit application entry point
├── style.css               # Custom UI styling
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (API keys)
├── chroma_db/              # Persistent vector database storage
└── core/
    ├── __init__.py
    ├── config.py           # Configuration management
    ├── llm.py              # Gemini AI client wrapper
    ├── memory.py           # ChromaDB memory manager
    └── orchestrator.py     # Core AI orchestration logic
```

### Core Components

| Component | Description |
|-----------|-------------|
| **Orchestrator** | The "brain" that coordinates memory retrieval and LLM generation |
| **MemoryManager** | Handles document storage, chunking, and semantic search |
| **GeminiClient** | Wrapper for Google's Gemini AI API |
| **Config** | Environment variable management and validation |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Google AI Studio API Key ([Get one here](https://aistudio.google.com/))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/phenothiazine/nexus-core.git
   cd nexus-core
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   # Create .env file
   echo "GOOGLE_API_KEY=your_api_key_here" > .env
   ```

5. **Run the application**
   ```bash
   streamlit run main.py
   ```

6. **Open your browser** at `http://localhost:8501`

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| [**Streamlit**](https://streamlit.io/) | Web application framework |
| [**Google Gemini**](https://ai.google.dev/) | Large Language Model |
| [**ChromaDB**](https://www.trychroma.com/) | Vector database for RAG |
| [**PyPDF**](https://pypdf.readthedocs.io/) | PDF document processing |

---

## 📖 Usage Guide

### 💾 Building Your Knowledge Base

1. **Add Notes**: Use the "Memory Bank" in the sidebar to save text notes
2. **Upload Files**: Import PDF or TXT files to expand your knowledge base
3. **Query Naturally**: Ask questions and Nexus will retrieve relevant context

### 💬 Chat Management

- **New Chat**: Click "➕ Start New Chat" to begin a fresh conversation
- **Switch Chats**: Click any chat in the sidebar to switch context
- **Rename**: Click the chat title header or use the ⋮ menu
- **Pin/Unpin**: Keep important chats at the top
- **Delete**: Remove chats you no longer need

---

## 🔧 Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GOOGLE_API_KEY` | ✅ | Your Google AI Studio API key |

### Customization

- **Model**: Change the model in `core/llm.py` (default: `gemini-3-flash-preview`)
- **Memory**: Adjust chunk size in `core/memory.py` for different document types
- **UI**: Modify `style.css` for custom theming

---

## 🗺️ Roadmap

- [ ] Multi-model support (OpenAI, Claude, Local LLMs)
- [ ] Voice input/output
- [ ] Web search integration
- [ ] Agent task execution
- [ ] Export/Import conversations
- [ ] Collaborative knowledge sharing

---

## 🤝 Contributing

Contributions are welcome! Feel free to:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [Google AI](https://ai.google.dev/) for Gemini API
- [Streamlit](https://streamlit.io/) for the amazing framework
- [ChromaDB](https://www.trychroma.com/) for vector database capabilities

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/phenothiazine">phenothiazine</a>
</p>

<p align="center">
  <strong>⭐ Star this repo if you find it useful!</strong>
</p>
