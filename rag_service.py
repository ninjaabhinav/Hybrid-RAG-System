from vectorstore.index_manager import IndexManager
from retrieval.multi_retriever import MultiRetriever
from router.mode_router import ModeRouter


class RAGService:
    def __init__(self):
        self.index_manager = IndexManager()
        self.router = ModeRouter()

    def index_document(self, file_path):
        """
        Build or load index for uploaded file.
        """
        self.index_manager.build_or_load_index(file_path)

    def answer_query(self, query, mode="offline"):
        """
        Retrieve from all indexed documents and generate answer.
        """
        stores = self.index_manager.load_all_indexes()

        if not stores:
            return "No documents indexed yet."

        retriever = MultiRetriever(stores)
        retrieved_docs = retriever.retrieve(query)

        if not retrieved_docs:
            return "No relevant content found."

        answer = self.router.answer(query, retrieved_docs, mode=mode)

        return answer