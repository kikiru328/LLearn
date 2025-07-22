from abc import ABCMeta, abstractmethod
from typing import Optional

from ulid import ULID

from curriculum.domain.entity.curriculum import Curriculum


class ICurriculumRepository(metaclass=ABCMeta):
    @abstractmethod
    async def save(self, curriculum: Curriculum):
        raise NotImplementedError

    @abstractmethod
    async def find_by_id(self, id: ULID) -> Optional[Curriculum]:
        raise NotImplementedError

    @abstractmethod
    async def find_curriculums(
        self, page: int, items_per_page: int
    ) -> tuple[int, list[Curriculum]]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, curriculum: Curriculum):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: ULID):
        raise NotImplementedError
