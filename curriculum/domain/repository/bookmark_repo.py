from abc import ABCMeta, abstractmethod
from typing import Optional, List, Tuple
from curriculum.domain.entity.bookmark import Bookmark


class IBookmarkRepository(metaclass=ABCMeta):
    @abstractmethod
    async def create(self, bookmark: Bookmark) -> None:
        raise NotImplementedError

    @abstractmethod
    async def find_by_user_and_curriculum(
        self, user_id: str, curriculum_id: str
    ) -> Optional[Bookmark]:
        raise NotImplementedError

    @abstractmethod
    async def delete_by_user_and_curriculum(
        self, user_id: str, curriculum_id: str
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def find_by_user(
        self, user_id: str, page: int = 1, items_per_page: int = 10
    ) -> Tuple[int, List[Bookmark]]:
        raise NotImplementedError

    @abstractmethod
    async def count_by_curriculum(self, curriculum_id: str) -> int:
        raise NotImplementedError
