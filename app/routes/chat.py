from fastapi import APIRouter

from app.models.schemas import ChatRequest

from app.services.vector_service import (
    get_context
)

from app.services.rag_service import (
    generate_answer
)

router = APIRouter(
    tags=["Chat"]
)


@router.post("/ask", summary="Ask a question about the loaded video")
def ask_question(data: ChatRequest):
    """
    Accepts a question and returns an AI-generated answer
    based on the currently loaded video's transcript context.
    """

    # Get context from vector DB
    context = get_context(
        data.question
    )

    # Debug Logs
    print("\n========== QUESTION ==========")
    print(data.question)

    print("\n========== CONTEXT ==========")
    print(context[:2000])

    print("\n========== END ==========\n")

    # Generate Answer
    answer = generate_answer(
        data.question,
        context
    )

    return {
        "question": data.question,
        "answer": answer
    }