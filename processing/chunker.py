from typing import List, Dict
from config import Config


config = Config()


def chunk_documents(documents: List[Dict]) -> List[Dict]:
    """
    Splits documents into overlapping chunks.
    Preserves metadata.
    """

    chunked_docs = []

    for doc in documents:
        text = doc["content"]
        metadata = doc["metadata"]

        chunks = split_text(text)

        for chunk in chunks:
            chunked_docs.append({
                "content": chunk,
                "metadata": metadata
            })

    return chunked_docs


def split_text(text: str) -> List[str]:
    """
    Splits text into chunks with overlap.
    """

    chunk_size = config.CHUNK_SIZE
    overlap = config.CHUNK_OVERLAP

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)

        start = end - overlap

    return chunks