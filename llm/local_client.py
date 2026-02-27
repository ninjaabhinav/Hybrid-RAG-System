import requests

class LocalLLMClient:
    def __init__(self, model_name="llama3"):
        self.model_name = model_name
        self.url = "http://localhost:11434/api/generate"

    def generate(self, context, query):
        prompt = f"""
You are a retrieval-augmented assistant.

Use ONLY the context below to answer the question.
If the answer is not in the context, say "Answer not found in the document."

Context:
{context}

Question:
{query}

Answer:
"""

        response = requests.post(
            self.url,
            json={
                "model": self.model_name,
                "prompt": prompt,
                "stream": False
            }
        )

        return response.json()["response"]