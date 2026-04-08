import re


def preprocess_text(text: str) -> str:
    lowered = text.lower().strip()
    normalized_space = re.sub(r"\s+", " ", lowered)
    return normalized_space


def extract_urls(text: str) -> list[str]:
    return re.findall(r"https?://[^\s]+|www\.[^\s]+", text.lower())
