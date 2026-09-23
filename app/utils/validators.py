import re

def validate_youtube_url(url: str) -> bool:
    """Returns True if the given URL is a valid YouTube link."""
    pattern = (
        r"(https?://)?"
        r"(www\.)?"
        r"(youtube\.com|youtu\.be)/"
    )

    return bool(re.match(pattern, url))

