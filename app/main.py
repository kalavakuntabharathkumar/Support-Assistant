from fastapi import FastAPI, HTTPException
from .schemas import AskRequest, AskResponse, Source
from .graph import support_graph

app = FastAPI(title="Agentic Support Assistant", version="1.0.0")
review_queue: list[dict] = []

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ask", response_model=AskResponse)
def ask(payload: AskRequest):
    try:
        result = support_graph.invoke({"question": payload.question})
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Assistant unavailable: {type(exc).__name__}")
    sources = [
        Source(article_id=x["article_id"], title=x["title"], url=x["url"], relevance=x["score"])
        for x in result.get("sources", [])
    ]
    response = AskResponse(
        answer=result.get("answer", "No answer generated."),
        sources=sources,
        confidence=round(float(result.get("confidence", 0.0)), 3),
        escalated=bool(result.get("escalated", True)),
        reason=result.get("reason"),
    )
    if response.escalated:
        review_queue.append({"question": payload.question, "answer": response.answer, "reason": response.reason})
    return response

@app.get("/review-queue")
def get_review_queue():
    return {"items": review_queue, "count": len(review_queue)}
