from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_answer(question, context):

    q = question.lower().strip()

    # Greetings
    greetings = [
        "hi",
        "hello",
        "hey",
        "hii",
        "hlo"
    ]

    if q in greetings:
        return "Hello! Ask me anything about the uploaded video."

    # Empty Context
    if not context or len(context.strip()) < 20:
        return "I could not find this information in the video."

    prompt = f"""
You are an Enterprise YouTube Video RAG Assistant.

IMPORTANT RULES:

1. Use ONLY the provided context.

2. Never use outside knowledge.

3. Never guess.

4. Never infer.

5. Never hallucinate.

6. If the answer is not explicitly available in the context, reply EXACTLY:

I could not find this information in the video.

7. Song lyrics are NOT song titles.

8. Transcript text does NOT automatically reveal:
   - song name
   - singer
   - actor
   - actress
   - movie name
   - creator
   - channel name

9. For summary questions:
   - summarize this video
   - what is this video about
   - explain this video

Generate a short summary ONLY from the provided context.

10. Answer in the same language as the user's question.

CONTEXT:
{context[:7000]}

QUESTION:
{question}

ANSWER:
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": """
You are a strict RAG assistant.

Answer only from retrieved context.

Never hallucinate.

Never guess.

If information is missing, reply:

I could not find this information in the video.
"""
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0,
        top_p=0.1,
        max_tokens=300
    )

    answer = (
        response
        .choices[0]
        .message.content
        .strip()
    )

    return answer