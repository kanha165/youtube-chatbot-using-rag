import chromadb

client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = client.get_or_create_collection(
    name="youtube_rag"
)

CURRENT_VIDEO_ID = None


def store_chunks(video_id, chunks):

    global CURRENT_VIDEO_ID

    CURRENT_VIDEO_ID = video_id

    if not chunks:
        raise ValueError(
            f"No chunks generated for video {video_id}"
        )

    # Delete old video chunks
    try:

        existing = collection.get()

        if existing["ids"]:

            collection.delete(
                ids=existing["ids"]
            )

    except Exception as e:

        print(
            "Delete Error:",
            e
        )

    ids = [
        f"{video_id}_{i}"
        for i in range(len(chunks))
    ]

    collection.add(
        ids=ids,
        documents=chunks,
        metadatas=[
            {
                "video_id": video_id
            }
            for _ in chunks
        ]
    )

    return True


def video_exists(video_id):

    results = collection.get(
        where={
            "video_id": video_id
        }
    )

    return len(results["ids"]) > 0


SUMMARY_QUERIES = [
    "summary",
    "summarize",
    "video about",
    "what is this video about",
    "explain this video",
    "video summary",
    "main topic",
    "video kis bare me hai",
    "video kis baare me hai"
]


def get_context(question):

    global CURRENT_VIDEO_ID

    if CURRENT_VIDEO_ID is None:
        return ""

    q = question.lower()

    # Summary questions
    if any(
        term in q
        for term in SUMMARY_QUERIES
    ):

        results = collection.get(
            where={
                "video_id": CURRENT_VIDEO_ID
            }
        )

        docs = results["documents"]

        return "\n".join(
            docs[:10]
        )

    # Normal retrieval

    results = collection.query(
        query_texts=[question],
        n_results=4,
        where={
            "video_id": CURRENT_VIDEO_ID
        }
    )

    docs = results["documents"][0]

    return "\n".join(docs)