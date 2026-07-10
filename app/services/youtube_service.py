import os
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import WebshareProxyConfig

load_dotenv()

PROXY_USERNAME = os.getenv("PROXY_USERNAME")
PROXY_PASSWORD = os.getenv("PROXY_PASSWORD")


def _get_api_client():
    """
    Returns YouTubeTranscriptApi client.
    Uses Webshare proxy if credentials are set in .env,
    otherwise falls back to direct connection (for local dev).
    """
    if PROXY_USERNAME and PROXY_PASSWORD:
        proxy_config = WebshareProxyConfig(
            proxy_username=PROXY_USERNAME,
            proxy_password=PROXY_PASSWORD,
        )
        return YouTubeTranscriptApi(proxies=proxy_config)

    # Local development - no proxy needed
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

    # Try Hindi first, then English, then any available language
    try:
        transcript = api.fetch(video_id, languages=["hi", "en"])
        return transcript

    except Exception:
        # Fallback: fetch whatever language is available
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
