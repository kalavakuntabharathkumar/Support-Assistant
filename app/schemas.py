from pydantic import BaseModel, Field

class AskRequest(BaseModel):
    question: str = Field(min_length=3, max_length=2000)

class Source(BaseModel):
    article_id: str
    title: str
    url: str
    relevance: float

class AskResponse(BaseModel):
    answer: str
    sources: list[Source]
    confidence: float
    escalated: bool
    reason: str | None = None
