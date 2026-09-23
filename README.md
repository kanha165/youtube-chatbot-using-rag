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

## 🔑 Prerequisites & Environment Variables

### Prerequisites
- Python 3.10+
- pip
- A free [Groq API key](https://console.groq.com) — for LLM inference
- A free [Supadata API key](https://supadata.ai) — for YouTube transcripts (100 req/month free)
- A MySQL database — for video metadata (optional, only needed if DB features are used)

### Environment Variables

Create a `.env` file in the project root:

```env
# Groq LLM
GROQ_API_KEY=your_groq_api_key_here

# Supadata (YouTube Transcript API)
SUPADATA_API_KEY=your_supadata_api_key_here

# MySQL Database (optional)
DATABASE_URL=mysql+pymysql://username:password@host:3306/dbname
```

| Variable | Required | Where to get |
|----------|----------|-------------|
| `GROQ_API_KEY` | ✅ Yes | [console.groq.com](https://console.groq.com) |
| `SUPADATA_API_KEY` | ✅ Yes | [supadata.ai](https://supadata.ai) |
| `DATABASE_URL` | ⚠️ Optional | Your MySQL provider |

> ⚠️ Never commit your `.env` file. It is already in `.gitignore`.

---

## ⚙️ Installation & Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/kanha165/youtube-chatbot-using-rag.git
cd youtube-chatbot-using-rag
```

### 2. Create and activate virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create your `.env` file

```bash
# Create .env in project root and add your keys
GROQ_API_KEY=your_groq_api_key_here
SUPADATA_API_KEY=your_supadata_api_key_here
DATABASE_URL=mysql+pymysql://user:pass@host:3306/dbname
```

### 5. Start the server

```bash
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### 6. Open the frontend

Open `frontend/index.html` directly in your browser.

> For local testing, edit line 2 of the `<script>` in `index.html`:
> ```js
> const API = "http://127.0.0.1:8000";
> ```

### 7. Test the API

Visit `http://127.0.0.1:8000/docs` for the interactive Swagger UI.

```bash
# Quick health check
curl http://127.0.0.1:8000/
# → {"message": "YouTube RAG Running"}
```

---

## 📡 API Endpoints

Base URL (local): `http://127.0.0.1:8000`  
Base URL (production): `https://youtube-chatbot-using-rag-hhzr.onrender.com`

---

### `GET /`
Health check — confirms the server is running.

**Response:**
```json
{ "message": "YouTube RAG Running" }
```

---

### `POST /process-video`
Fetches transcript from a YouTube video, chunks it, and stores it in ChromaDB.

**Request Body:**
```json
{ "url": "https://www.youtube.com/watch?v=VIDEO_ID" }
```

**Response (success):**
```json
{
  "status": "success",
  "video_id": "VIDEO_ID",
  "transcript_length": 4821,
  "total_chunks": 11,
  "preview": "First 500 chars of transcript..."
}
```

**Response (already processed):**
```json
{
  "status": "already_processed",
  "video_id": "VIDEO_ID",
  "message": "Video already exists in ChromaDB"
}
```

---

### `POST /ask`
Ask any question about the currently loaded video.

**Request Body:**
```json
{ "question": "What is this video about?" }
```

**Response:**
```json
{
  "question": "What is this video about?",
  "answer": "This video is about..."
}
```

---

### `GET /count`
Returns the total number of chunks stored in ChromaDB.

**Response:**
```json
{ "documents": 11 }
```

---

## 🚀 Deployment Guide (Render)

This project is deployed on [Render](https://render.com) (free tier).

### Steps to deploy your own instance

**1. Push your code to GitHub**
```bash
git push origin main
```

**2. Create a new Web Service on Render**
- Go to [render.com](https://render.com) → New → Web Service
- Connect your GitHub repo

**3. Configure the service**

| Setting | Value |
|---------|-------|
| **Runtime** | Python 3 |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |

**4. Add Environment Variables**

In Render dashboard → Environment → Add:
```
GROQ_API_KEY        = your_groq_api_key
SUPADATA_API_KEY    = your_supadata_api_key
DATABASE_URL        = your_mysql_connection_string
```

**5. Deploy**
- Click **Deploy** — Render will install deps and start the server
- Your API will be live at `https://your-app-name.onrender.com`

**6. Update frontend**

In `frontend/index.html`, update the API base URL:
```js
const API = "https://your-app-name.onrender.com";
```

> 💡 **Note:** Render free tier spins down after 15 min of inactivity. First request after sleep may take ~30 seconds.

---
