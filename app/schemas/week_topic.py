from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional
from uuid import UUID
from datetime import datetime

# 다른 Schema에서 임베드용 (SaveCurriculumRequest에서 사용)
class WeekTopicData(BaseModel):
    week_number: int = Field(..., ge=1, description="주차 번호")
    title: str = Field(..., min_length=1, max_length=100, description="주차 제목")
    description: str = Field(..., description="주차 설명")
    learning_goals: List[str] = Field(..., min_length=1, description="학습 목표 리스트")

# 조회 응답용 (나중에 WeekTopic 개별 조회할 때)
class WeekTopicResponse(BaseModel):
    id: UUID
    curriculum_id: UUID
    week_number: int
    title: str
    description: str
    learning_goals: List[str]
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# 수정 요청용 (나중에 필요하면)
class UpdateWeekTopicRequest(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100, description="주차 제목")
    description: Optional[str] = Field(None, description="주차 설명")
    learning_goals: Optional[List[str]] = Field(None, min_length=1, description="학습 목표 리스트")