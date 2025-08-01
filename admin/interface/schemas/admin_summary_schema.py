from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

from curriculum.domain.entity.summary import Summary
from curriculum.domain.entity.feedback import Feedback


class AdminFeedbackResponse(BaseModel):
    """Admin용 피드백 응답"""

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


class AdminGetSummaryResponse(BaseModel):
    """Admin 전용 Summary 조회 응답 - 모든 정보 포함"""

    id: str
    curriculum_id: str
    week_number: int
    content: str
    created_at: datetime
    updated_at: datetime
    feedback: Optional[AdminFeedbackResponse]

    @classmethod
    def from_domain(
        cls, summary: Summary, feedback: Optional[Feedback] = None
    ) -> "AdminGetSummaryResponse":
        return cls(
            id=summary.id,
            curriculum_id=summary.curriculum_id,
            week_number=summary.week_number.value,
            content=summary.content.value,
            created_at=summary.created_at,
            updated_at=summary.updated_at,
            feedback=AdminFeedbackResponse.from_domain(feedback) if feedback else None,
        )


class AdminGetSummariesPageResponse(BaseModel):
    """Admin 전용 Summary 목록 응답"""

    total_count: int
    page: int
    items_per_page: int
    summaries: List[AdminGetSummaryResponse]

    @classmethod
    def from_domain(
        cls,
        total_count: int,
        page: int,
        items_per_page: int,
        summaries: List[AdminGetSummaryResponse],
    ) -> "AdminGetSummariesPageResponse":
        return cls(
            total_count=total_count,
            page=page,
            items_per_page=items_per_page,
            summaries=summaries,
        )
