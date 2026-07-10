import chromadb

client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = client.get_or_create_collection(
    name="youtube_rag"
)


def _load_current_video_id():
    """
    Server restart pe ChromaDB se last stored video_id load karo.
    """
    try:
        existing = collection.get()
        if existing["metadatas"]:
            return existing["metadatas"][0].get("video_id", None)
    except Exception:
        pass
    return None


# Startup pe ChromaDB se restore karo
CURRENT_VIDEO_ID = _load_current_video_id()


def store_chunks(video_id, chunks):

    global CURRENT_VIDEO_ID

    if not chunks:
        raise ValueError(
            f"No chunks generated for video {video_id}"
        )

    # Delete old video chunks
    try:
        existing = collection.get()
        if existing["ids"]:
            collection.delete(ids=existing["ids"])
    except Exception as e:
        print("Delete Error:", e)

    ids = [
        f"{video_id}_{i}"
        for i in range(len(chunks))
    ]

    collection.add(
        ids=ids,
        documents=chunks,
        metadatas=[
            {"video_id": video_id}
            for _ in chunks
        ]
    )

    CURRENT_VIDEO_ID = video_id
    return True


def video_exists(video_id):
    results = collection.get(
        where={"video_id": video_id}
    )
    return len(results["ids"]) > 0


# Summary detect karne ke liye keywords — English + Hindi
SUMMARY_KEYWORDS = [
    # English
    "summary", "summarize", "summarise", "overview",
    "what is this video", "what is the video", "video about",
    "explain this video", "explain the video",
    "what does this video", "tell me about this video",
    "what happened in", "main topic", "main points",
    "key points", "what was discussed", "what was talked",
    "describe this video", "describe the video",
    # Hindi / Hinglish
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


def get_context(question: str) -> str:

    global CURRENT_VIDEO_ID

    if CURRENT_VIDEO_ID is None:
        CURRENT_VIDEO_ID = _load_current_video_id()

    if CURRENT_VIDEO_ID is None:
        return ""

    # Summary → saare chunks do (poora transcript)
    if is_summary_question(question):
        results = collection.get(
            where={"video_id": CURRENT_VIDEO_ID}
        )
        docs = results.get("documents", [])
        # Saare chunks join karo — 7000 char limit rag_service handle karega
        return "\n".join(docs)

    # Normal question → semantic search se top 5 relevant chunks
    results = collection.query(
        query_texts=[question],
        n_results=5,
        where={"video_id": CURRENT_VIDEO_ID}
    )

    docs = results["documents"][0]
    return "\n".join(docs)
