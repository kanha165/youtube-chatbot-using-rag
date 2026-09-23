# ChromaDB handles embeddings internally using its built-in ONNX model.
# sentence-transformers is not needed — this file is kept for reference only.

def create_embeddings(chunks):
    """
    Deprecated: ChromaDB auto-embeds documents on collection.add().
    This function is no longer called anywhere in the codebase.
    """
    raise NotImplementedError(
        "ChromaDB handles embeddings internally. "
        "Call collection.add(documents=chunks) directly."
    )
