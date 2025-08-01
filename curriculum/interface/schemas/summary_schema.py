from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class CreateSummaryReqeust(BaseModel):
    content: str = Field(
        min_length=100,
        max_length=5000,
        description="요약 본문 (500~1,000자)",
    )


class SummaryBriefResponse(BaseModel):
    id: str
    curriculum_id: str
    snippet: str
    created_at: datetime

    @classmethod
    def from_domain(cls, summary):
        snippet = summary.content.value[:30] + "..."
        return cls(
            id=summary.id,
            curriculum_id=summary.curriculum_id,
            snippet=snippet,
            created_at=summary.created_at,
        )


class FeedbackResponse(BaseModel):
    id: str
    comment: str
    score: float
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_domain(cls, feedback):
        return cls(
            id=feedback.id,
            comment=feedback.comment.value,
            score=feedback.score.value,
            created_at=feedback.created_at,
            updated_at=getattr(feedback, "updated_at", feedback.created_at),
        )


class SummaryDetailResponse(BaseModel):
    id: str
    content: str
    created_at: datetime
    updated_at: datetime
    feedback: Optional[FeedbackResponse]

    @classmethod
    def from_domain(cls, summary, feedback=None):
        return cls(
            id=summary.id,
            content=summary.content.value,
            created_at=summary.created_at,
            updated_at=getattr(summary, "updated_at", summary.created_at),
            feedback=FeedbackResponse.from_domain(feedback) if feedback else None,
        )


SummaryDetailResponse.model_rebuild()


class SummaryPageResponse(BaseModel):
    total_count: int
    summaries: List[SummaryBriefResponse]

    @classmethod
    def from_domain(cls, total_count: int, summaries: List) -> "SummaryPageResponse":
        briefs = [SummaryBriefResponse.from_domain(s) for s in summaries]
        return cls(total_count=total_count, summaries=briefs)
