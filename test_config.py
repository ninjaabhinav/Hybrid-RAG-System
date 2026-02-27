from rag_service import RAGService

rag = RAGService()

# Index documents (run once per file)
rag.index_document("sample.pdf")
# rag.index_document("another.pdf")  # optional

query = "What technologies are used?"
answer = rag.answer_query(query, mode="offline")

print(answer)