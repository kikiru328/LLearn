from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from domain.entities.feedback import Feedback


class FeedbackRepository(ABC):
    """피드백 저장소 인터페이스"""

    @abstractmethod
    async def save(self, feedback: Feedback) -> Feedback:
        """피드백 저장"""
        pass

    @abstractmethod
    async def find_by_id(self, feedback_id: UUID) -> Optional[Feedback]:
        """ID로 피드백 조회"""
        pass

    @abstractmethod
    async def find_by_summary_id(self, summary_id: UUID) -> Optional[Feedback]:
        """요약에 대한 피드백 조회 (요약당 피드백 1개)"""
        pass

    @abstractmethod
    async def find_all(self) -> List[Feedback]:
        """전체 피드백 조회 (관리자용)"""
        pass

    @abstractmethod
    async def delete(self, feedback_id: UUID) -> None:
        """피드백 삭제"""
        pass