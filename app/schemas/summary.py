from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID

class CreateSummaryRequest(BaseModel):
    week_topic_id: UUID = Field(
        ...,
        description="주차 ID"
    )
    content: str = Field(
        ...,
        min_length=50,
        max_length=5000,
        description="주차별 요약문"
    )

    is_public: bool = Field(
        default=False,
        description="공개 여부"
    )

class UpdateSummaryRequest(BaseModel):
    content: Optional[str] = Field(
        None,
        min_length=50,
        max_length=5000,
        description="주차별 요약문"
    )
    
    is_public: Optional[bool] = Field(
        None,
        description="공개 여부"
    )
    
class SummaryResponse(BaseModel):
    id: UUID
    user_id: UUID
    week_topic_id: UUID
    content: str
    is_public: bool
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
    
    
class ListSummaryResponse(BaseModel):
    summaries: List[SummaryResponse]
    total: int
    page: int
    size: int
    has_next: bool
    