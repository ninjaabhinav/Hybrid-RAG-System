from google import genai
from config import Config


config = Config()


class GeminiClient:
    def __init__(self):
        self.client = genai.Client(api_key=config.GEMINI_API_KEY)
        self.model_name = "models/gemini-2.5-flash"

    # -----------------------------
    # Prompt Builders
    # -----------------------------

    def build_offline_prompt(self, context, query):
        return f"""
You are a document-grounded AI assistant.

STRICT RULES:
- Use the information provided in the context below.
- Do NOT use outside knowledge.
- Try to find specific contexts that could imporve the answer size and quality.
- If the answer is not present in the context, respond exactly with:
"Answer not found in the document."

Context:
{context}

Question:
{query}

Provide a clear, structured answer based strictly on the context.
"""

    def build_online_prompt(self, context, query):
        return f"""
You are an intelligent assistant using hybrid retrieval.

INSTRUCTIONS:
- First, use the provided context.
- If the context partially answers the question, expand logically.
- If the context does not contain relevant information,
  answer using your general knowledge.

Context:
{context}

Question:
{query}

Provide a detailed, well-structured explanation.
Clearly prioritize document-based information when available.
"""

    # -----------------------------
    # Main Generate Method
    # -----------------------------

    def generate(self, context, query, mode="offline"):

        if mode == "offline":
            prompt = self.build_offline_prompt(context, query)
        else:
            prompt = self.build_online_prompt(context, query)

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
        )

        return response.text
    