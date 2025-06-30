from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class GenerateFeedbackUseCaseRequest:
    """GenerateFeedbackUseCase 입력 DTO"""
    summary_id: UUID


@dataclass
class GenerateFeedbackUseCaseResponse:
    """GenerateFeedbackUseCase 출력 DTO"""
    id: UUID
    summary_id: UUID
    content: str  # 5단계 구조화된 피드백
    created_at: datetime