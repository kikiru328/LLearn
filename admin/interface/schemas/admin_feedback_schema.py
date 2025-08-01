from datetime import datetime
from typing import List
from pydantic import BaseModel

from curriculum.domain.entity.feedback import Feedback


class AdminGetFeedbackResponse(BaseModel):
    """Admin 전용 Feedback 조회 응답 - 모든 정보 포함"""

    id: str
    summary_id: str
    comment: str
    score: float
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_domain(cls, feedback: Feedback) -> "AdminGetFeedbackResponse":
        return cls(
            id=feedback.id,
            summary_id=feedback.summary_id,
            comment=feedback.comment.value,
            score=feedback.score.value,
            created_at=feedback.created_at,
            updated_at=feedback.updated_at,
        )


class AdminGetFeedbacksPageResponse(BaseModel):
    """Admin 전용 Feedback 목록 응답"""

    total_count: int
    page: int
    items_per_page: int
    feedbacks: List[AdminGetFeedbackResponse]

    @classmethod
    def from_domain(
        cls,
        total_count: int,
        page: int,
        items_per_page: int,
        feedbacks: List[AdminGetFeedbackResponse],
    ) -> "AdminGetFeedbacksPageResponse":
        return cls(
            total_count=total_count,
            page=page,
            items_per_page=items_per_page,
            feedbacks=feedbacks,
        )
