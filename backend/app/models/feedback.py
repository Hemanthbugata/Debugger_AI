from pydantic import BaseModel
from typing import Optional

class FeedbackRequest(BaseModel):
    debug_request: dict
    response: dict
    rating: int
    comment: Optional[str] = None