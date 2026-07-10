import os
import requests
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi

load_dotenv()

PROXY_USERNAME = os.getenv("PROXY_USERNAME")
PROXY_PASSWORD = os.getenv("PROXY_PASSWORD")


def _get_api_client():
    """
    Webshare free plan ke shared proxies use karta hai.
    p.webshare.io:80 Webshare ka backbone rotating endpoint hai —
    free plan mein bhi kaam karta hai.
    """
    if PROXY_USERNAME and PROXY_PASSWORD:

        # Webshare backbone proxy — free plan ke saath kaam karta hai
        proxy_url = (
            f"http://{PROXY_USERNAME}:{PROXY_PASSWORD}"
            f"@p.webshare.io:80"
        )

        session = requests.Session()
        session.proxies = {
            "http":  proxy_url,
            "https": proxy_url,
        }

        return YouTubeTranscriptApi(http_client=session)

    # Local development — direct connection
    return YouTubeTranscriptApi()


def extract_video_id(url):

    parsed_url = urlparse(url)

    if "youtu.be" in parsed_url.netloc:
        return parsed_url.path.lstrip("/")

    if "youtube.com" in parsed_url.netloc:
        query = parse_qs(parsed_url.query)
        return query.get("v", [None])[0]

    return None


def get_transcript(video_id: str):

    api = _get_api_client()

    # Hindi ya English transcript try karo
    try:
        transcript = api.fetch(video_id, languages=["hi", "en"])
        return transcript

    except Exception:
        # Fallback: koi bhi available language
        try:
            transcript_list = api.list(video_id)
            first = next(iter(transcript_list))
            transcript = first.fetch()
            return transcript

        except Exception as e:
            raise RuntimeError(
                f"Could not fetch transcript for video '{video_id}': {e}"
            )


def transcript_to_text(transcript):

    if not transcript:
        return ""

    return " ".join(
        snippet.text
        for snippet in transcript
    )


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
