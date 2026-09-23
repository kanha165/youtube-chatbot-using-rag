<div align="center">

# 🎬 VideoRAG — AI YouTube Chatbot

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-0.136-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/ChromaDB-1.5.9-orange?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Groq-LLM-red?style=for-the-badge" />
  <img src="https://img.shields.io/badge/RAG-Architecture-purple?style=for-the-badge" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" />
</p>

<p align="center">
  <strong>Ask anything about any YouTube video — powered by RAG (Retrieval-Augmented Generation)</strong>
</p>

<p align="center">
  Paste a YouTube URL → Get the transcript → Ask questions in English, Hindi, or Hinglish → Get accurate AI answers
</p>

<p align="center">
  <a href="https://youtube-chatbot-using-rag-hhzr.onrender.com" target="_blank">
    🚀 Live Demo
  </a>
  &nbsp;&nbsp;|&nbsp;&nbsp;
  <a href="#-installation--local-setup">
    ⚙️ Local Setup
  </a>
  &nbsp;&nbsp;|&nbsp;&nbsp;
  <a href="#-api-endpoints">
    📡 API Docs
  </a>
</p>

</div>

---

## ✨ Features

- 🎥 **YouTube Transcript Extraction** — Fetches transcripts from any YouTube video via Supadata API (no IP blocking issues)
- 🧠 **RAG Pipeline** — Splits transcript into chunks, embeds them, stores in ChromaDB, retrieves relevant context per question
- 💬 **Multilingual Chat** — Ask in **English**, **Hindi**, or **Hinglish** — answers in the same language
- 📝 **Smart Summary** — Detects summary questions and returns full transcript context automatically
- ⚡ **Groq LLM** — Ultra-fast inference using `qwen/qwen3.8-27b` model
- 🔍 **Semantic Search** — Top-7 relevant chunks retrieved using vector similarity
- 🗄️ **Persistent Storage** — ChromaDB persists data across server restarts
- 🌐 **Clean UI** — Dark-themed responsive frontend, no framework needed
- 🔄 **Duplicate Detection** — Same video won't be re-processed if already in DB
- 🚀 **Production Ready** — Deployed on Render with CORS support

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Backend** | FastAPI | REST API framework |
| **LLM** | Groq — `qwen/qwen3.8-27b` | Answer generation |
| **Embeddings** | `sentence-transformers` — `all-MiniLM-L6-v2` | Text → vector conversion |
| **Vector DB** | ChromaDB | Semantic search & storage |
| **Transcript** | Supadata API | YouTube transcript fetching |
| **Database** | SQLAlchemy + PyMySQL | Video metadata storage |
| **Frontend** | Vanilla HTML/CSS/JS | Chat UI (no framework) |
| **Server** | Uvicorn | ASGI server |
| **Deployment** | Render | Cloud hosting |
| **Env Mgmt** | python-dotenv | API key management |

---
