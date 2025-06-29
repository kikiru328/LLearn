from datetime import datetime
from typing import List
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field

from app.schemas.summary import SummaryResponse


class FeedbackResponse(BaseModel):
    id: UUID
    summary_id: UUID
    content: str = Field(
        ...,
        description="5단계 구조화된 피드백"
    )
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
    
class ListFeedbackResponse(BaseModel):
    feedbacks: List[FeedbackResponse]
    total: int
    page: int
    size: int
    has_next: bool
    
class FeedbackWithSummaryResponse(BaseModel):
    feedback: FeedbackResponse
    summary: SummaryResponse = Field(
        ...,
        description="피드백 대상 요약"
    )
    
    
    