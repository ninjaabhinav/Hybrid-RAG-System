from embeddings.embedder import Embedder
import numpy as np


class MultiRetriever:
    def __init__(self, stores):
        self.stores = stores
        self.embedder = Embedder()

    def retrieve(self, query, top_k=5):
        query_embedding = self.embedder.embed_query(query)

        all_results = []

        for store in self.stores:
            results = store.search(query_embedding, top_k=top_k)
            all_results.extend(results)

        return all_results