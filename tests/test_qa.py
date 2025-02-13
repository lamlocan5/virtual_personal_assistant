import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.rag import RAGService
from unittest.mock import AsyncMock, patch

client = TestClient(app)

@pytest.fixture
def mock_rag_service():
    with patch('app.routers.qa.rag_service') as mock:
        mock.process_question = AsyncMock()
        mock.process_question.return_value = "This is a test answer"
        yield mock

def test_ask_question_endpoint(mock_rag_service):
    response = client.post(
        "/qa/ask",
        json={
            "question": "What is the meaning of life?",
            "context": "Philosophy context"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "sentiment" in data
    assert "confidence" in data

def test_feedback_endpoint():
    response = client.post(
        "/qa/feedback",
        json={
            "question_id": "test_id",
            "feedback": "Great answer!",
            "rating": 5
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"

@pytest.mark.asyncio
async def test_rag_service():
    service = RAGService()
    
    # Test question processing
    question = "What is Python?"
    context = "Python is a programming language"
    
    with patch('openai.AsyncOpenAI') as mock_openai:
        mock_openai.return_value.chat.completions.create = AsyncMock()
        mock_openai.return_value.chat.completions.create.return_value.choices = [
            type('obj', (object,), {
                'message': type('obj', (object,), {
                    'content': 'Python is a versatile programming language'
                })
            })
        ]
        
        response = await service.process_question(question, context)
        assert isinstance(response, str)
        assert len(response) > 0

def test_invalid_question():
    response = client.post(
        "/qa/ask",
        json={
            "question": "",  # Empty question should fail
            "context": None
        }
    )
    
    assert response.status_code == 422  # Validation error