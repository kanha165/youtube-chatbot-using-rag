from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

def create_embeddings(chunks):
    """Convert text chunks into vector embeddings using sentence-transformers."""
    embeddings = model.encode(
        chunks
    )

    return embeddings