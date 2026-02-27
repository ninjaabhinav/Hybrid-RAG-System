import faiss
import numpy as np
import os
import pickle
from config import Config


config = Config()


class FAISSStore:
    def __init__(self, dimension):
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.metadata = []

    def add_embeddings(self, embeddings, documents):
        self.index.add(embeddings)
        self.metadata.extend(documents)

    def search(self, query_embedding, top_k=None):
        if top_k is None:
            top_k = config.TOP_K

        distances, indices = self.index.search(
            np.array([query_embedding]), top_k
        )

        results = []
        for idx in indices[0]:
            if idx < len(self.metadata):
                results.append(self.metadata[idx])

        return results

    def save(self, path):
        os.makedirs(path, exist_ok=True)
        faiss.write_index(self.index, os.path.join(path, "index.faiss"))

        with open(os.path.join(path, "metadata.pkl"), "wb") as f:
            pickle.dump(self.metadata, f)

    def load(self, path):
        self.index = faiss.read_index(os.path.join(path, "index.faiss"))

        with open(os.path.join(path, "metadata.pkl"), "rb") as f:
            self.metadata = pickle.load(f)