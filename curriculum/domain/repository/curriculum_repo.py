from abc import ABCMeta, abstractmethod
from typing import List, Optional, Tuple
from curriculum.domain.entity.curriculum import Curriculum
from curriculum.domain.value_object.title import Title
from user.domain.value_object.role import RoleVO


class ICurriculumRepository(metaclass=ABCMeta):
    @abstractmethod
    async def create(self, curriculum: Curriculum) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, curriculum: Curriculum) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def count_owner(self, owner_id: str) -> int:
        """해당 유저가 만든 커리큘럼 개수 반환"""
        raise NotImplementedError

    @abstractmethod
    async def find_by_id(
        self,
        id: str,
        role: RoleVO,
        owner_id: Optional[str] = None,
    ):
        raise NotImplementedError

    @abstractmethod
    async def find_by_title(
        self,
        title: Title,
        role: RoleVO,
        owner_id: Optional[str] = None,
    ) -> Optional[Curriculum]:
        raise NotImplementedError

    @abstractmethod
    async def find_curriculums(
        self,
        page: int,
        items_per_page: int,
        role: RoleVO,
        owner_id: Optional[str] = None,
    ) -> Tuple[int, List[Curriculum]]:
        raise NotImplementedError

    @abstractmethod
    async def insert_week_and_shift(
        self,
        curriculum_id: str,
        new_week_number: int,
        lessons: List[str],
    ):
        raise NotImplementedError

    @abstractmethod
    async def delete_week_and_shift(
        self,
        curriculum_id: str,
        week_number: int,
    ):
        raise NotImplementedError

    @abstractmethod
    async def insert_lesson(
        self,
        curriculum_id: str,
        week_number: int,
        lesson: str,
        lesson_index: int,
    ):
        raise NotImplementedError

    @abstractmethod
    async def update_week_schedule(
        self,
        curriculum_id: str,
        week_number: int,
        lessons: List[str],
    ):
        raise NotImplementedError

    @abstractmethod
    async def delete_lesson(
        self,
        curriculum_id: str,
        week_number: int,
        lesson_index: int,
    ):
        raise NotImplementedError
