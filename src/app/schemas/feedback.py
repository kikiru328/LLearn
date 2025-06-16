from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class FeedbackResponse(BaseModel):
    id: UUID
    summary_id: UUID
    reviewer: str
    content: str
    created_at: datetime