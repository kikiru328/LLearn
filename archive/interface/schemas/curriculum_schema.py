from datetime import datetime
from pydantic import BaseModel, Field
from typing import Annotated, List


# ─── 재사용 Body ───


class WeekScheduleBody(BaseModel):
    week_number: int = Field(..., gt=0, description="주차 번호")
    topics: Annotated[
        List[str],
        Field(..., min_items=1, description="주차별 학습 주제 목록"),
    ]


class SummaryBody(BaseModel):
    week_number: int = Field(..., gt=0, description="주차 번호")
    content: str = Field(..., min_length=1, max_length=1000, description="요약 내용")


class FeedbackBody(BaseModel):
    summary_id: str = Field(..., description="요약 ID")
    comment: str = Field(..., min_length=1, max_length=500, description="피드백 댓글")
    score: int = Field(..., ge=0, le=10, description="피드백 점수")


# ─── Request Models ───


class CurriculumGenerateRequest(BaseModel):
    topic: str = Field(..., description="학습 주제")
    duration_weeks: int = Field(
        ...,
        ge=1,
        le=24,
        description="학습 기간(주 단위, 1~24주)",
    )


class CurriculumUpdateRequest(BaseModel):
    topic: str = Field(..., description="새 커리큘럼 제목")


class SummaryRequest(BaseModel):
    week_number: int = Field(..., ge=1, description="주차 번호")
    content: str = Field(..., min_length=1, max_length=1000, description="요약 내용")


class FeedbackRequest(BaseModel):
    summary_id: str = Field(..., description="요약 ID")
    comment: str = Field(..., min_length=1, max_length=500, description="피드백 댓글")
    score: int = Field(..., ge=0, le=10, description="피드백 점수")


# ─── Response Models ───


class CurriculumResponse(BaseModel):
    id: str
    owner_id: str
    topic: str
    duration_weeks: int
    week_schedules: List[WeekScheduleBody]
    created_at: datetime
    updated_at: datetime


class SummaryResponse(BaseModel):
    id: str
    content: str
    submitted_at: datetime


class FeedbackResponse(BaseModel):
    id: str
    comment: str
    score: int
    created_at: datetime


class PaginatedCurriculumsResponse(BaseModel):
    total_count: int
    page: int
    items_per_page: int
    curriculums: List[CurriculumResponse]
