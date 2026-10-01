# Agentic Support Assistant with LangGraph

A multi-step support assistant that routes a query, retrieves evidence from a ChromaDB knowledge base, drafts a cited answer, and escalates uncertain requests.

## Architecture
1. FastAPI accepts a support question.
2. A LangGraph workflow classifies the intent and decides whether retrieval is needed.
3. LangChain creates embeddings and queries ChromaDB.
4. Azure OpenAI drafts an answer grounded in retrieved article snippets.
5. A confidence gate routes weak evidence to a human-review queue.

## Quick start
Python 3.11+ is recommended.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Add Azure OpenAI endpoint, key, deployment names and API version.
python scripts/ingest_articles.py --input data/articles.jsonl
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs`.

## API
- `POST /ask` — ask a question; returns answer, sources, confidence and escalation status.
- `GET /health` — service health.
- `GET /review-queue` — list in-memory escalations (replace with durable storage for production).

Example:
```json
{"question":"How do I reset my password?"}
```

## Knowledge articles
`data/articles.jsonl` contains a small, clearly-labelled starter corpus. Replace it with your 150 public support articles in JSONL format (`id`, `title`, `content`, `url`). The repository does not redistribute third-party articles.

## Evaluation
```bash
python scripts/evaluate.py --input data/eval_questions.jsonl
```
The evaluation script computes exact-label grounded-answer pass rate from the supplied hand-labelled examples. The project brief's reported 61% baseline and 83% routed-system result are target/reported figures, not a guarantee that this starter corpus reproduces them. Re-run evaluation with the original 120 labelled questions before making performance claims.

## Docker / Azure Container Apps
```bash
docker build -t support-assistant .
docker run --env-file .env -p 8000:8000 support-assistant
```
For Azure Container Apps, create a container app with ingress on port 8000 and configure secrets/environment variables in the Azure portal or CLI. Never commit `.env` or credentials.

## Notes
The review queue is process-local for demonstration. Use Azure Service Bus, Cosmos DB or PostgreSQL for durable multi-replica review workflows. Add authentication, rate limiting, PII handling and observability before production use.
