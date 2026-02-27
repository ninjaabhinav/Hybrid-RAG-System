from config import Config

config = Config()

try:
    from tavily import TavilyClient
except ImportError:
    TavilyClient = None


class WebSearch:
    def __init__(self):
        if config.TAVILY_API_KEY and TavilyClient:
            self.client = TavilyClient(api_key=config.TAVILY_API_KEY)
        else:
            self.client = None

    def search(self, query, max_results=3):
        if not self.client:
            return []

        response = self.client.search(
            query=query,
            max_results=max_results
        )

        results = []

        for r in response["results"]:
            results.append({
                "content": r["content"],
                "metadata": {
                    "source": r["url"],
                    "type": "web"
                }
            })

        return results