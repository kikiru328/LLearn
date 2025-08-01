from abc import ABCMeta, abstractmethod
from typing import List, Optional, Tuple
from curriculum.domain.entity.summary import Summary


class ISummaryRepository(metaclass=ABCMeta):
    @abstractmethod
    async def create(self, summary: Summary) -> None:
        raise NotImplementedError

    @abstractmethod
    async def find_all_by_curriculum_and_week(
        self,
        curriculum_id: str,
        week_number: int,
        page: int = 1,
        items_per_page: int = 10,
    ) -> Tuple[int, List[Summary]]:
        raise NotImplementedError

    @abstractmethod
    async def find_by_id(self, id: str) -> Optional[Summary]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def find_all_by_user(
        self,
        owner_id: str,
        page: int,
        items_per_page: int,
    ) -> Tuple[int, List[Summary]]:
        raise NotImplementedError

    @abstractmethod
    async def find_all_summaries_for_admin(
        self,
        page: int = 1,
        items_per_page: int = 10,
    ) -> Tuple[int, List[Summary]]:
        raise NotImplementedError

    @abstractmethod
    async def count_all_summaries(self) -> int:
        raise NotImplementedError
