import os
from dotenv import load_dotenv

load_dotenv()

def required(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value

def settings():
    return {
        "endpoint": required("AZURE_OPENAI_ENDPOINT"),
        "key": required("AZURE_OPENAI_API_KEY"),
        "api_version": os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21"),
        "chat_deployment": required("AZURE_OPENAI_CHAT_DEPLOYMENT"),
        "embedding_deployment": required("AZURE_OPENAI_EMBEDDING_DEPLOYMENT"),
        "chroma_path": os.getenv("CHROMA_PATH", "./storage/chroma"),
        "threshold": float(os.getenv("CONFIDENCE_THRESHOLD", "0.55")),
    }
