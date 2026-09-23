import chromadb
from chromadb.config import Settings

# EphemeralClient — no disk persistence needed on Render
# PersistentClient locally (path="chroma_db")
import os

if os.getenv("RENDER"):
    # Render pe in-memory client — no ONNX download, no disk issues
    client = chromadb.EphemeralClient()
else:
    # Local pe persistent storage
    client = chromadb.PersistentClient(path="chroma_db")


# No embedding_function → ChromaDB will NOT download any ONNX model
# We handle retrieval manually via keyword search
from chromadb.utils.embedding_functions import EmbeddingFunction

class NoEmbedding(EmbeddingFunction):
    """
    Dummy embedding — stores chunks as-is.
    We do our own keyword-based retrieval so we don't need vectors.
    """
    def __call__(self, input):
        # Return a fixed 1-dim vector — ChromaDB needs something
        return [[0.0] for _ in input]

collection = client.get_or_create_collection(
    name="youtube_rag_v2",
    embedding_function=NoEmbedding()
)


def _load_current_video_id():
    """Server restart pe ChromaDB se last stored video_id load karo."""
    try:
        existing = collection.get()
        if existing["metadatas"]:
            return existing["metadatas"][0].get("video_id", None)
    except Exception:
        pass
    return None


# Startup pe restore karo
CURRENT_VIDEO_ID = _load_current_video_id()


def store_chunks(video_id, chunks):
    global CURRENT_VIDEO_ID

    if not chunks:
        raise ValueError(f"No chunks generated for video {video_id}")

    # Delete old video chunks
    try:
        existing = collection.get()
        if existing["ids"]:
            collection.delete(ids=existing["ids"])
    except Exception as e:
        print("Delete Error:", e)

    ids = [f"{video_id}_{i}" for i in range(len(chunks))]

    collection.add(
        ids=ids,
        documents=chunks,
        metadatas=[{"video_id": video_id} for _ in chunks]
    )

    CURRENT_VIDEO_ID = video_id
    return True


def video_exists(video_id):
    """Check if a video's chunks are already stored in ChromaDB."""
    results = collection.get(where={"video_id": video_id})
    return len(results["ids"]) > 0


# Summary detect karne ke liye keywords — English + Hindi
SUMMARY_KEYWORDS = [
    "summary", "summarize", "summarise", "overview",
    "what is this video", "what is the video", "video about",
    "explain this video", "explain the video",
    "what does this video", "tell me about this video",
    "what happened in", "main topic", "main points",
    "key points", "what was discussed", "what was talked",
    "describe this video", "describe the video",
    "is video me kya", "is video mein kya",
    "video kis bare", "video kis baare",
    "video ka summary", "video ka matlab",
    "video me kya hai", "video mein kya hai",
    "batao is video", "is video ko samjhao",
    "video explain karo", "video samjhao",
    "kya hai is video", "kya chal raha hai",
    "iske baare mein batao", "video ke baare mein",
]


def is_summary_question(question: str) -> bool:
    q = question.lower()
    return any(kw in q for kw in SUMMARY_KEYWORDS)


def _keyword_search(question: str, chunks: list, top_n: int = 7) -> list:
    """
    Simple keyword-based retrieval — no ONNX, no vectors needed.
    Score each chunk by how many question words appear in it.
    """
    words = set(question.lower().split())
    # Remove very short/common words
    stopwords = {"a", "an", "the", "is", "in", "on", "of", "and", "or",
                 "to", "for", "with", "this", "that", "it", "at", "by",
                 "kya", "hai", "ka", "ke", "ki", "ko", "me", "mein", "se",
                 "ne", "karo", "do", "tha", "thi", "hain", "ho", "what",
                 "how", "why", "when", "where", "who", "which", "does"}
    words = words - stopwords

    scored = []
    for chunk in chunks:
        chunk_lower = chunk.lower()
        score = sum(1 for w in words if w in chunk_lower)
        scored.append((score, chunk))

    # Sort by score descending, return top_n
    scored.sort(key=lambda x: x[0], reverse=True)
    return [chunk for _, chunk in scored[:top_n]]


def get_context(question: str) -> str:
    global CURRENT_VIDEO_ID

    if CURRENT_VIDEO_ID is None:
        CURRENT_VIDEO_ID = _load_current_video_id()

    if CURRENT_VIDEO_ID is None:
        return ""

    # Get all chunks for current video
    results = collection.get(where={"video_id": CURRENT_VIDEO_ID})
    all_chunks = results.get("documents", [])

    if not all_chunks:
        return ""

    # Summary → return all chunks (full transcript)
    if is_summary_question(question):
        return "\n".join(all_chunks)

    # Normal question → keyword search, top 7 relevant chunks
    relevant = _keyword_search(question, all_chunks, top_n=7)
    return "\n".join(relevant)
