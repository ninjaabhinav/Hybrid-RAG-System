from sentence_transformers import SentenceTransformer
import numpy as np
from config import Config


config = Config()


class Embedder:
    def __init__(self):
        self.model = SentenceTransformer(
        config.EMBEDDING_MODEL_NAME,
        local_files_only=True
        )

    def embed_texts(self, texts):
        """
        Takes list of strings and returns numpy embeddings
        """
        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=True
        )
        return embeddings

    def embed_query(self, query):
        """
        Embeds single query
        """
        return self.model.encode(query, convert_to_numpy=True)