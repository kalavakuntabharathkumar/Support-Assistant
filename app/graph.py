from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from .config import settings
from .retrieval import retrieve

class SupportState(TypedDict, total=False):
    question: str
    route: str
    sources: list[dict]
    answer: str
    confidence: float
    escalated: bool
    reason: str

def classify(state: SupportState):
    q = state["question"].lower()
    account_terms = ("password", "account", "login", "email", "invoice", "billing", "refund")
    return {"route": "retrieve" if any(term in q for term in account_terms) else "general"}

def search(state: SupportState):
    try:
        hits = retrieve(state["question"])
        return {"sources": hits}
    except Exception as exc:
        return {"sources": [], "reason": f"Retrieval unavailable: {type(exc).__name__}"}

def draft(state: SupportState):
    cfg = settings()
    llm = AzureChatOpenAI(
        azure_endpoint=cfg["endpoint"],
        api_key=cfg["key"],
        api_version=cfg["api_version"],
        azure_deployment=cfg["chat_deployment"],
        temperature=0,
    )
    context = "\n\n".join(
        f"[{x['article_id']}] {x['title']} ({x['url']}): {x['content']}"
        for x in state.get("sources", [])
    )
    if not context:
        return {"answer": "I could not find reliable support documentation for this request.", "confidence": 0.0}
    messages = [
        SystemMessage(content=(
            "You are a careful support assistant. Answer only from the supplied sources. "
            "If the sources do not answer the question, say so. Cite supporting article IDs "
            "in square brackets. Do not invent policies."
        )),
        HumanMessage(content=f"Question: {state['question']}\n\nSources:\n{context}"),
    ]
    result = llm.invoke(messages)
    scores = [x["score"] for x in state.get("sources", [])]
    confidence = max(scores, default=0.0)
    return {"answer": result.content, "confidence": confidence}

def gate(state: SupportState):
    threshold = settings()["threshold"]
    weak = state.get("confidence", 0.0) < threshold
    return {
        "escalated": weak,
        "reason": state.get("reason") or ("Low retrieval confidence" if weak else None),
    }

def build_graph():
    graph = StateGraph(SupportState)
    graph.add_node("classify", classify)
    graph.add_node("retrieve", search)
    graph.add_node("draft", draft)
    graph.add_node("gate", gate)
    graph.set_entry_point("classify")
    graph.add_conditional_edges("classify", lambda s: s["route"], {
        "retrieve": "retrieve",
        "general": "retrieve",
    })
    graph.add_edge("retrieve", "draft")
    graph.add_edge("draft", "gate")
    graph.add_edge("gate", END)
    return graph.compile()

support_graph = build_graph()
