from datetime import datetime
from pydantic import BaseModel

from curriculum.domain.entity.feedback import Feedback


class FeedbackResponse(BaseModel):
    id: str
    comment: str
    score: float
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_domain(cls, feedback: Feedback):
        return cls(
            id=feedback.id,
            comment=feedback.comment.value,
            score=feedback.score.value,
            created_at=feedback.created_at,
            updated_at=feedback.updated_at,
        )


class CreateFeedbackRequest(BaseModel):
    pass
