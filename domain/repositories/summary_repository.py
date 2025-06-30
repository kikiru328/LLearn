from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from domain.entities.summary import Summary


class SummaryRepository(ABC):
    """요약 저장소 인터페이스"""

    @abstractmethod
    async def save(self, summary: Summary) -> Summary:
        """요약 저장 (생성/수정)"""
        pass

    @abstractmethod
    async def find_by_id(self, summary_id: UUID) -> Optional[Summary]:
        """ID로 요약 조회"""
        pass

    @abstractmethod
    async def find_by_user_id(self, user_id: UUID) -> List[Summary]:
        """사용자의 요약 목록 조회"""
        pass

    @abstractmethod
    async def find_by_week_topic_id(self, week_topic_id: UUID) -> Optional[Summary]:
        """주차별 요약 조회 (한 주차당 요약 1개)"""
        pass

    @abstractmethod
    async def find_public_summaries(self) -> List[Summary]:
        """공개된 요약 피드 조회"""
        pass
    
    @abstractmethod
    async def find_by_week_topic_id_and_public(self, week_topic_id: UUID, is_public: bool) -> List[Summary]:
        """특정 주차의 공개/비공개 요약들 조회"""
        pass
    
    @abstractmethod
    async def find_all(self) -> List[Summary]:
        """전체 요약 조회 (관리자용)"""
        pass

    @abstractmethod
    async def delete(self, summary_id: UUID) -> None:
        """요약 삭제"""
        pass