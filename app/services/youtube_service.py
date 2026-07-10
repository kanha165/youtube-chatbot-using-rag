import os
import requests
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv

load_dotenv()

SUPADATA_API_KEY = os.getenv("SUPADATA_API_KEY")

SUPADATA_URL = "https://api.supadata.ai/v1/youtube/transcript"


def extract_video_id(url):

    parsed_url = urlparse(url)

    if "youtu.be" in parsed_url.netloc:
        return parsed_url.path.lstrip("/")

    if "youtube.com" in parsed_url.netloc:
        query = parse_qs(parsed_url.query)
        return query.get("v", [None])[0]

    return None


def get_transcript(video_id: str):
    """
    Supadata API se transcript fetch karo.
    Yeh YouTube ke IP blocks se safe hai — dedicated service hai.
    Free tier: 100 requests/month (no credit card needed)
    """

    if not SUPADATA_API_KEY:
        raise RuntimeError(
            "SUPADATA_API_KEY not set in environment variables."
        )

    response = requests.get(
        SUPADATA_URL,
        headers={
            "x-api-key": SUPADATA_API_KEY
        },
        params={
            "videoId": video_id,
            "text": "true"   # plain text transcript return karo
        },
        timeout=30
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"Supadata API error {response.status_code}: {response.text}"
        )

    data = response.json()

    # Supadata text=true pe plain string return karta hai content mein
    content = data.get("content", "")

    if not content or not content.strip():
        raise RuntimeError(
            f"No transcript content found for video '{video_id}'"
        )

    return content


def transcript_to_text(transcript):
    """
    Supadata already plain text deta hai — seedha return karo.
    """
    if not transcript:
        return ""
    return transcript


def chunk_text(
        text,
        chunk_size=1000,
        overlap=200
):

    if not text or not text.strip():
        raise ValueError("Transcript text is empty. Cannot create chunks.")

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += (chunk_size - overlap)

    return chunks
