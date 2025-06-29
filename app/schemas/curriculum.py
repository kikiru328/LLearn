from datetime import datetime
from typing import List
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from app.schemas.week_topic import WeekTopicData, WeekTopicResponse



class GenerateCurriculumRequest(BaseModel):
    goal: str = Field(
        ..., 
        min_length=5,
        max_length=200,
        description="학습 목표")
    
    duration_weeks: int = Field(
        default=12,
        ge=1,
        le=26, 
        description="학습 목표 기간(주)")

class SaveCurriculumRequest(BaseModel):
    goal: str = Field(..., min_length=5, max_length=200, description="학습 목표")
    duration_weeks: int = Field(..., ge=1, le=26, description="학습 기간(주)")
    title: str = Field(..., min_length=1, max_length=30, description="커리큘럼 제목")
    weeks: List[WeekTopicData] = Field(..., description="주차별 학습 내용")
    is_public: bool = Field(default=False, description="공개 여부")
    
class CurriculumSummary(BaseModel):
    """each curriculum summary for display in list curriculums"""
    id: UUID
    title: str
    goal: str
    duration_weeks: int
    is_public: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
    
class CurriculumResponse(BaseModel):
    id: UUID
    user_id: UUID
    goal: str
    title: str
    duration_weeks: int
    is_public: bool
    created_at: datetime
    updated_at: datetime
    weeks: List[WeekTopicResponse] = Field(..., description="주차별 학습 내용")
    
    model_config = ConfigDict(from_attributes=True)
    
class ListCurriculumResponse(BaseModel):
    curriculums: List[CurriculumSummary]
    total: int
    page: int
    size: int
    has_next: bool