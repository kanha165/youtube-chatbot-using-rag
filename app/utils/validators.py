import re

def validate_youtube_url(url: str):

    pattern = (
        r"(https?://)?"
        r"(www\.)?"
        r"(youtube\.com|youtu\.be)/"
    )

    return bool(re.match(pattern, url))

