import os
from embeddings.embedder import Embedder
from vectorstore.faiss_store import FAISSStore
from processing.cleaner import clean_text
from processing.chunker import chunk_documents
from ingestion.pdf_loader import load_pdf
from ingestion.ppt_loader import load_ppt
from config import Config


config = Config()


class IndexManager:
    def __init__(self):
        self.embedder = Embedder()

    def _get_index_path(self, doc_name):
        safe_name = doc_name.replace(" ", "_").split(".")[0]
        return os.path.join(config.INDEX_DIR, safe_name)

    def build_or_load_index(self, file_path):
        doc_name = os.path.basename(file_path)
        index_path = self._get_index_path(doc_name)

        if os.path.exists(os.path.join(index_path, "index.faiss")):
            print("Loading existing index...")
            store = FAISSStore(dimension=384)  # MiniLM dimension
            store.load(index_path)
            return store

        print("Building new index...")

        # Load document
        if file_path.lower().endswith(".pdf"):
            docs = load_pdf(file_path)
        elif file_path.lower().endswith((".ppt", ".pptx")):
            docs = load_ppt(file_path)
        else:
            raise ValueError("Unsupported file format")

        # Clean
        for doc in docs:
            doc["content"] = clean_text(doc["content"])

        # Chunk
        chunks = chunk_documents(docs)
        texts = [chunk["content"] for chunk in chunks]

        # Embed
        embeddings = self.embedder.embed_texts(texts)

        dimension = embeddings.shape[1]
        store = FAISSStore(dimension)
        store.add_embeddings(embeddings, chunks)

        # Save
        store.save(index_path)

        return store
    def load_all_indexes(self):
        stores = []

        for folder in os.listdir(config.INDEX_DIR):
            index_path = os.path.join(config.INDEX_DIR, folder)
            index_file = os.path.join(index_path, "index.faiss")

            if os.path.exists(index_file):
                try:
                    store = FAISSStore(dimension=384)
                    store.load(index_path)
                    stores.append(store)
                except Exception:
                    print(f"Skipping corrupted index: {folder}")

        return stores