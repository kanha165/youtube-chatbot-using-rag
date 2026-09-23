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

## 🏗️ Architecture & How It Works

```
User pastes YouTube URL
        │
        ▼
┌─────────────────────┐
│   FastAPI Backend   │
│  POST /process-video│
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│   Supadata API      │  ← Fetches full transcript (IP-safe)
└────────┬────────────┘
         │  plain text transcript
         ▼
┌─────────────────────┐
│   chunk_text()      │  ← Split into 1000-char chunks (200 overlap)
└────────┬────────────┘
         │  list of chunks
         ▼
┌─────────────────────┐
│  SentenceTransformer│  ← all-MiniLM-L6-v2 embeddings
└────────┬────────────┘
         │  vectors
         ▼
┌─────────────────────┐
│     ChromaDB        │  ← Persistent vector store
└─────────────────────┘

User asks a question
        │
        ▼
┌─────────────────────┐
│   POST /ask         │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  is_summary_question│  ← Summary? → fetch ALL chunks
│  OR semantic search │  ← Normal? → top-7 similar chunks
└────────┬────────────┘
         │  context
         ▼
┌─────────────────────┐
│    Groq LLM         │  ← qwen/qwen3.8-27b generates answer
└────────┬────────────┘
         │
         ▼
      Answer returned to user
```

### Flow Summary
1. **Video Processing** — URL → transcript → chunks → embeddings → ChromaDB
2. **Question Answering** — Question → vector search → relevant chunks → Groq LLM → answer
3. **Language Detection** — Hindi/English/Hinglish question → answer in same language

---

## 📁 Project Structure

```
youtube-chatbot-using-rag/
│
├── app/
│   ├── main.py                    # FastAPI app entry point, CORS setup
│   │
│   ├── routes/
│   │   ├── video.py               # POST /process-video, GET /count
│   │   └── chat.py                # POST /ask
│   │
│   ├── services/
│   │   ├── youtube_service.py     # Supadata API — transcript fetching & chunking
│   │   ├── embedding_service.py   # SentenceTransformer — text → vectors
│   │   ├── vector_service.py      # ChromaDB — store, search, retrieve chunks
│   │   └── rag_service.py         # Groq LLM — prompt building & answer generation
│   │
│   ├── models/
│   │   └── schemas.py             # Pydantic request/response models
│   │
│   ├── database/
│   │   ├── db.py                  # SQLAlchemy engine & session setup
│   │   ├── models.py              # Video ORM model
│   │   └── __init__.py
│   │
│   └── utils/
│       └── validators.py          # YouTube URL validator
│
├── frontend/
│   └── index.html                 # Complete chat UI (HTML/CSS/JS)
│
├── chroma_db/                     # ChromaDB persistent storage (auto-created)
│
├── .env                           # Environment variables (not committed)
├── .gitignore
├── requirements.txt
└── README.md
```

---
