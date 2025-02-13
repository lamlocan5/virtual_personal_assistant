from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Optional
from app.services.rag import RAGService
from app.utils.sentiment import analyze_sentiment

router = APIRouter()
rag_service = RAGService()

@router.post("/ask")
async def ask_question(
    question: str,
    context: Optional[str] = None
) -> Dict:
    """
    Process a question using RAG and return an answer
    """
    try:
        answer = await rag_service.process_question(question, context)
        sentiment = analyze_sentiment(answer)
        
        return {
            "answer": answer,
            "sentiment": sentiment,
            "confidence": 0.95
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/feedback")
async def provide_feedback(
    question_id: str,
    feedback: str,
    rating: int
) -> Dict:
    """
    Submit feedback for a previous question-answer interaction
    """
    return {
        "status": "success",
        "message": "Feedback recorded successfully"
    }