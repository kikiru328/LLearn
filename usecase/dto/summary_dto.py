from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class CreateSummaryUseCaseRequest:
    """CreateSummaryUseCase 입력 DTO"""
    user_id: UUID
    week_topic_id: UUID
    content: str
    is_public: bool = False


@dataclass
class CreateSummaryUseCaseResponse:
    """CreateSummaryUseCase 출력 DTO"""
    id: UUID
    user_id: UUID
    week_topic_id: UUID
    content: str
    is_public: bool
    created_at: datetime
    updated_at: datetime