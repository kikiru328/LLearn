from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from domain.entities.week_topic import WeekTopic


class WeekTopicRepository(ABC):
    """주차별 주제 저장소 인터페이스"""

    @abstractmethod
    async def save(self, week_topic: WeekTopic) -> WeekTopic:
        """주차별 주제 저장 (생성/수정)"""
        pass

    @abstractmethod
    async def find_by_id(self, week_topic_id: UUID) -> Optional[WeekTopic]:
        """ID로 주차별 주제 조회"""
        pass

    @abstractmethod
    async def find_by_curriculum_id(self, curriculum_id: UUID) -> List[WeekTopic]:
        """커리큘럼의 모든 주차 조회"""
        pass

    @abstractmethod
    async def find_by_curriculum_and_week(self, curriculum_id: UUID, week_number: int) -> Optional[WeekTopic]:
        """특정 커리큘럼의 특정 주차 조회"""
        pass

    @abstractmethod
    async def find_all(self) -> List[WeekTopic]:
        """전체 주차별 주제 조회 (관리자용)"""
        pass

    @abstractmethod
    async def delete(self, week_topic_id: UUID) -> None:
        """주차별 주제 삭제"""
        pass