from fastapi import APIRouter

from app.models.schemas import VideoRequest

from app.services.youtube_service import (
    extract_video_id,
    get_transcript,
    transcript_to_text,
    chunk_text
)

from app.services.vector_service import (
    store_chunks,
    video_exists,
    collection
)

router = APIRouter(
    tags=["Videos"]
)


@router.post("/process-video")
def process_video(data: VideoRequest):

    video_id = extract_video_id(
        data.url
    )

    if not video_id:
        return {
            "status": "error",
            "message": "Invalid YouTube URL"
        }

    try:

        # Already processed
        if video_exists(video_id):
            return {
                "status": "already_processed",
                "video_id": video_id,
                "message": "Video already exists in ChromaDB"
            }

        # Get transcript
        transcript = get_transcript(
            video_id
        )

        # Convert transcript to text
        text = transcript_to_text(
            transcript
        )

        # Create chunks
        chunks = chunk_text(
            text
        )

        # Store in vector DB
        store_chunks(
            video_id,
            chunks
        )

        return {
            "status": "success",
            "video_id": video_id,
            "transcript_length": len(text),
            "total_chunks": len(chunks),
            "preview": text[:500]
        }

    except Exception as e:

        return {
            "status": "error",
            "video_id": video_id,
            "message": str(e)
        }


@router.get("/count")
def count_documents():

    return {
        "documents": collection.count()
    }