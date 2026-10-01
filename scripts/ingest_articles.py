import argparse, json
from pathlib import Path
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import AzureOpenAIEmbeddings
from app.config import settings

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/articles.jsonl")
    args = parser.parse_args()
    cfg = settings()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=80)
    docs = []
    with open(args.input, encoding="utf-8") as handle:
        for line in handle:
            row = json.loads(line)
            for chunk in splitter.split_text(row["content"]):
                docs.append(Document(page_content=chunk, metadata={
                    "article_id": row["id"], "title": row["title"], "url": row["url"]
                }))
    if not docs:
        raise SystemExit("No article documents found.")
    embeddings = AzureOpenAIEmbeddings(
        azure_endpoint=cfg["endpoint"], api_key=cfg["key"],
        api_version=cfg["api_version"], azure_deployment=cfg["embedding_deployment"]
    )
    Chroma.from_documents(
        docs, embeddings, collection_name="support_articles",
        persist_directory=cfg["chroma_path"]
    )
    print(f"Indexed {len(docs)} chunks.")

if __name__ == "__main__":
    main()
