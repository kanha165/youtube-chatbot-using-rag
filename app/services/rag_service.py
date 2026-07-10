from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# Greetings — inpe seedha reply, context ki zarurat nahi
GREETINGS = [
    "hi", "hello", "hey", "hii", "hlo", "helo", "heyy",
    "namaste", "namaskar", "ram ram",
    "kya haal hai", "kaise ho", "how are you",
    "good morning", "good evening", "good afternoon", "good night",
    "sup", "yo", "wassup", "what's up", "whats up",
]

# Small talk — fixed replies
SMALL_TALK = {
    "what is your name":    "I'm VideoRAG — your AI assistant for YouTube videos!",
    "who are you":          "I'm VideoRAG, an AI chatbot that answers questions about YouTube videos.",
    "what can you do":      "I can summarize YouTube videos and answer any questions about them. Just load a video and ask!",
    "aap kaun ho":          "Main VideoRAG hoon — ek AI assistant jo YouTube videos ke sawaalon ke jawaab deta hai!",
    "tumhara naam kya hai": "Mera naam VideoRAG hai!",
    "tera naam kya hai":    "Mera naam VideoRAG hai!",
    "help":                 "Sidebar mein YouTube URL paste karo, Load Video dabaao, phir kuch bhi poochho!",
    "smj nhi rhe":          "Poochho kya jaanna chahte ho is video ke baare mein — main poori koshish karunga!",
    "samajh nahi":          "Batao kya poochh rahe ho — main madad karunga!",
    "kya kar sakte ho":     "YouTube video load karo aur uske baare mein kuch bhi poochho — summary, topics, details sab!",
}


def _is_greeting(q: str) -> bool:
    return q in GREETINGS or any(q == g or q.startswith(g + " ") for g in GREETINGS)


def _small_talk_reply(q: str):
    for key, reply in SMALL_TALK.items():
        if key in q:
            return reply
    return None


def generate_answer(question: str, context: str) -> str:

    q = question.lower().strip()

    # 1. Greetings
    if _is_greeting(q):
        return "Hello! 👋 Ask me anything about the loaded video."

    # 2. Small talk
    reply = _small_talk_reply(q)
    if reply:
        return reply

    # 3. No context
    if not context or len(context.strip()) < 20:
        return (
            "Video ka context nahi mila. "
            "Pehle ek YouTube URL load karo, phir sawaal karo."
        )

    prompt = f"""You are VideoRAG, a smart and friendly AI assistant that helps users understand YouTube videos.

Below is the full transcript/context from the video:

--- VIDEO TRANSCRIPT START ---
{context[:8000]}
--- VIDEO TRANSCRIPT END ---

User's question: {question}

Your task:
- If the user asks for a SUMMARY or "what is this video about" → Write a detailed, accurate summary covering all the main points from the transcript. Use bullet points if helpful.
- If the user asks a SPECIFIC question → Answer it directly using only information from the transcript above.
- If the user is making SMALL TALK (smj nahi, explain karo, etc.) → Respond helpfully and invite them to ask about the video.
- Always answer in the SAME LANGUAGE as the user's question:
  * Hindi question → Hindi answer
  * English question → English answer
  * Hinglish question → Hinglish answer
- Do NOT make up anything not present in the transcript.
- If information is truly not in the transcript, say: "Yeh information video mein nahi mili." (or English equivalent)
- Be clear, helpful, and conversational.

Answer:"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are VideoRAG, a helpful YouTube video AI assistant. "
                    "Answer based only on the video transcript provided. "
                    "Match the user's language (Hindi/English/Hinglish). "
                    "For summaries, be thorough and detailed. "
                    "For casual conversation, be warm and friendly."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.4,
        top_p=0.9,
        max_tokens=800
    )

    return response.choices[0].message.content.strip()
