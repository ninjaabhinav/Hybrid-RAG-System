from rag_service import RAGService

rag = RAGService()

# Index document (safe to call multiple times)
rag.index_document("sample.pdf")

query = "What technologies are used?"
answer = rag.answer_query(query, mode="offline")

print("\nAnswer:\n")
print(answer)