from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from domain.entities.curriculum import Curriculum


class CurriculumRepository(ABC):
    """curriculum repository interface"""

    @abstractmethod
    async def save(self, curriculum: Curriculum) -> Curriculum:
        """커리큘럼 저장 (생성/수정)"""
        pass

    @abstractmethod
    async def find_by_id(self, curriculum_id: UUID) -> Optional[Curriculum]:
        """ID로 커리큘럼 조회"""
        pass

    @abstractmethod
    async def find_by_user_id(self, user_id: UUID) -> List[Curriculum]:
        """사용자의 커리큘럼 목록 조회"""
        pass

    @abstractmethod
    async def find_public_curriculums(self) -> List[Curriculum]:
        """공개된 커리큘럼 목록 조회"""
        pass

    @abstractmethod
    async def find_all(self) -> List[Curriculum]:
        """전체 커리큘럼 조회 (관리자용) """
        pass

    @abstractmethod
    async def delete(self, curriculum_id: UUID) -> None:
        """커리큘럼 삭제"""
        pass