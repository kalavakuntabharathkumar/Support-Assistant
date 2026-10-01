from pathlib import Path
from langchain_chroma import Chroma
from langchain_openai import AzureOpenAIEmbeddings
from .config import settings

def vector_store():
    cfg = settings()
    embeddings = AzureOpenAIEmbeddings(
        azure_endpoint=cfg["endpoint"],
        api_key=cfg["key"],
        api_version=cfg["api_version"],
        azure_deployment=cfg["embedding_deployment"],
    )
    return Chroma(
        collection_name="support_articles",
        embedding_function=embeddings,
        persist_directory=cfg["chroma_path"],
    )

def retrieve(question: str, k: int = 4):
    docs = vector_store().similarity_search_with_relevance_scores(question, k=k)
    results = []
    for doc, score in docs:
        results.append({
            "article_id": doc.metadata.get("article_id", "unknown"),
            "title": doc.metadata.get("title", "Support article"),
            "url": doc.metadata.get("url", ""),
            "content": doc.page_content,
            "score": max(0.0, min(1.0, float(score))),
        })
    return results
