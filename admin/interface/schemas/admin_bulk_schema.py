from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

from curriculum.domain.value_object.visibility import Visibility


class BulkDeleteCurriculumsRequest(BaseModel):
    """커리큘럼 일괄 삭제 요청"""

    curriculum_ids: List[str] = Field(
        min_items=1, description="삭제할 커리큘럼 ID 목록"
    )


class BulkDeleteCurriculumsResponse(BaseModel):
    """커리큘럼 일괄 삭제 응답"""

    deleted_count: int
    deleted_ids: List[str]
    failed_count: int
    failed_items: List[Dict[str, Any]]  # {"id": "...", "error": "..."}


class BulkUpdateCurriculumsRequest(BaseModel):
    """커리큘럼 일괄 수정 요청"""

    curriculum_ids: List[str] = Field(
        min_items=1, description="수정할 커리큘럼 ID 목록"
    )
    title: Optional[str] = Field(
        None, min_length=2, max_length=50, description="새 제목"
    )
    visibility: Optional[Visibility] = Field(None, description="새 공개 설정")


class BulkUpdateCurriculumsResponse(BaseModel):
    """커리큘럼 일괄 수정 응답"""

    updated_count: int
    updated_ids: List[str]
    failed_count: int
    failed_items: List[Dict[str, Any]]  # {"id": "...", "error": "..."}


class BulkDeleteUsersRequest(BaseModel):
    """사용자 일괄 삭제 요청"""

    user_ids: List[str] = Field(min_items=1, description="삭제할 사용자 ID 목록")


class BulkDeleteUsersResponse(BaseModel):
    """사용자 일괄 삭제 응답"""

    deleted_count: int
    deleted_ids: List[str]
    failed_count: int
    failed_items: List[Dict[str, Any]]  # {"id": "...", "error": "..."}


class BulkDeleteSummariesRequest(BaseModel):
    """요약 일괄 삭제 요청"""

    summary_ids: List[str] = Field(min_items=1, description="삭제할 요약 ID 목록")


class BulkDeleteSummariesResponse(BaseModel):
    """요약 일괄 삭제 응답"""

    deleted_count: int
    deleted_ids: List[str]
    failed_count: int
    failed_items: List[Dict[str, Any]]  # {"id": "...", "error": "..."}


class BulkDeleteFeedbacksRequest(BaseModel):
    """피드백 일괄 삭제 요청"""

    feedback_ids: List[str] = Field(min_items=1, description="삭제할 피드백 ID 목록")


class BulkDeleteFeedbacksResponse(BaseModel):
    """피드백 일괄 삭제 응답"""

    deleted_count: int
    deleted_ids: List[str]
    failed_count: int
    failed_items: List[Dict[str, Any]]  # {"id": "...", "error": "..."}
