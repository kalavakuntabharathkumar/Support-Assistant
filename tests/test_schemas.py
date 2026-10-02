from app.schemas import AskRequest

def test_question_length_validation():
    assert AskRequest(question="How do I reset my password?").question.startswith("How")
