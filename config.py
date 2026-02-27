import os
from dotenv import load_dotenv


class Config:
    """
    Central configuration manager.
    Loads environment variables and global settings.
    """

    def __init__(self):
        # Load .env only for local development
        load_dotenv()

        # API Keys
        self.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        self.TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

        # Embedding model
        self.EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

        # Retrieval settings
        self.TOP_K = 3          # Reduce for performance
        self.CHUNK_SIZE = 700   # Slightly smaller for Streamlit memory
        self.CHUNK_OVERLAP = 100

        # Storage paths
        self.UPLOAD_DIR = "storage/uploads"
        self.INDEX_DIR = "storage/indexes"

        # Validate critical settings
        self._validate()

    def _validate(self):
        if not self.GEMINI_API_KEY:
            raise RuntimeError(
                "GEMINI_API_KEY not found. "
                "Set it in your .env file locally or in Streamlit Cloud Secrets."
            )

        if not self.TAVILY_API_KEY:
            print("TAVILY_API_KEY not set. Web search disabled.")