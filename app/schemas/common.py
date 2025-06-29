from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


# Request Paging for query parameter
class PaginationRequest(BaseModel):
    page: int = Field(1, ge=1, description="페이지 번호")
    size: int = Field(20, ge=1, le=100, description="페이지 크기")

# Response
class PaginationResponse(BaseModel):
    total: int = Field(..., description="전체 아이템 수")
    page: int = Field(..., description="현재 페이지")
    size: int = Field(..., description="페이지 크기")
    has_next: bool = Field(..., description="다음 페이지 존재 여부")

# Response Error
class ErrorResponse(BaseModel):
    detail: str
    error_code: Optional[str] = None

# Response Success
class SuccessResponse(BaseModel):
    message: str = Field(default="Success", description="성공 메시지")

# common field mixin
class TimestampMixin(BaseModel):
    created_at: datetime
    updated_at: datetime
    
# public mixin
class PublicMixin(BaseModel):
    is_public: bool = Field(default=False, description="공개 여부")