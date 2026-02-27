from llm.gemini_client import GeminiClient
from llm.local_client import LocalLLMClient

class ModeRouter:
    def __init__(self):
        self.online_llm = GeminiClient()
        self.offline_llm = LocalLLMClient()

    def answer(self, query, context, mode="offline"):
        if mode == "online":
            return self.online_llm.generate(context, query)
        else:
            return self.offline_llm.generate(context, query)