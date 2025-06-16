from pydantic import BaseModel, Field
from uuid import UUID
from typing import List
from datetime import datetime

# 1. 주차 단위 스키마
class WeekTopicSchema(BaseModel):
    week_number: int = Field(..., ge=1)
    topic: str

# 2. 커리큘럼 생성 요청
class CurriculumCreateRequest(BaseModel):
    title: str
    goal: str
    is_public: bool
    weeks: List[WeekTopicSchema]

# 3. 커리큘럼 생성 응답
class CurriculumCreateResponse(BaseModel):
    id: UUID
    title: str
    created_at: datetime

# 4. 커리큘럼 상세 조회
class CurriculumDetailResponse(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    goal: str
    is_public: bool
    weeks: List[WeekTopicSchema]
    created_at: datetime
    updated_at: datetime

# 5. 커리큘럼 목록 응답
class CurriculumSummaryResponse(BaseModel):
    id: UUID
    title: str
    is_public: bool
    created_at: datetime

# 6. 커리큘럼 수정 요청
class CurriculumUpdateRequest(BaseModel):
    title: str
    goal: str
    is_public: bool

# 7. 수정 응답
class CurriculumUpdateResponse(BaseModel):
    id: UUID
    updated_at: datetime