from fastapi import APIRouter
from app.models.feedback import FeedbackRequest
from app.feedback.feedback import FeedbackProcessor

router = APIRouter()
processor = FeedbackProcessor()

@router.post("/", summary="Submit feedback about the debugging result")
async def submit_feedback(feedback: FeedbackRequest):
    return processor.process(feedback.dict())