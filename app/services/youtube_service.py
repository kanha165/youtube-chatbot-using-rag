from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi


def extract_video_id(url):

    parsed_url = urlparse(url)

    if "youtu.be" in parsed_url.netloc:

        return parsed_url.path.lstrip("/")

    if "youtube.com" in parsed_url.netloc:

        query = parse_qs(
            parsed_url.query
        )

        return query.get(
            "v",
            [None]
        )[0]

    return None

def get_transcript(video_id: str):

    try:
        transcript = YouTubeTranscriptApi().fetch(
            video_id,
            languages=["hi", "en"]
        )

        return transcript

    except Exception as e:

        print("Transcript Error:", e)

        return None


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

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunks.append(
            text[start:end]
        )

        start += (
            chunk_size - overlap
        )

    return chunks