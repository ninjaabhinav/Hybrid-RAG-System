import re


def clean_text(text: str) -> str:
    """
    Cleans raw extracted text:
    - Removes excessive whitespace
    - Normalizes line breaks
    - Removes non-printable characters
    """

    # Remove non-printable characters
    text = re.sub(r"[^\x20-\x7E\n]", " ", text)

    # Normalize multiple newlines
    text = re.sub(r"\n\s*\n", "\n\n", text)

    # Remove excessive spaces
    text = re.sub(r"[ \t]+", " ", text)

    return text.strip()