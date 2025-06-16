from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime

# 요약 생성 요청
class SummaryCreateRequest(BaseModel):
    curriculum_id: UUID
    week_number: int = Field(..., ge=1)
    content: str
    is_public: bool = False

# 생성 응답
class SummaryCreateResponse(BaseModel):
    id: UUID
    created_at: datetime

# 요약 상세 조회 응답
class SummaryDetailResponse(BaseModel):
    id: UUID
    user_id: UUID
    curriculum_id: UUID
    week_number: int
    content: str
    is_public: bool
    created_at: datetime
    updated_at: datetime

# 피드용 요약 응답 (목록)
class SummaryFeedItem(BaseModel):
    id: UUID
    user_id: UUID
    nickname: str
    curriculum_title: str
    week_number: int
    content_preview: str
    created_at: datetime
    like_count: int
    comment_count: int