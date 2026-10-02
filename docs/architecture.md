# Workflow design

The LangGraph state carries the user question, route, retrieved evidence, draft answer and confidence gate result. Classification currently uses a transparent keyword router so the demo is deterministic; replace it with a structured Azure OpenAI classifier if you have a labelled intent set. Retrieval is shared across intents and the answer node is constrained to supplied evidence. The final gate sends low-scoring retrievals to the review queue.
