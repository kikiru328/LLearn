from abc import ABCMeta, abstractmethod
from typing import Optional, List, Tuple
from curriculum.domain.entity.category import Category
from curriculum.domain.value_object.category_name import CategoryName


class ICategoryRepository(metaclass=ABCMeta):
    @abstractmethod
    async def create(self, category: Category) -> None:
        raise NotImplementedError

    @abstractmethod
    async def find_by_id(self, category_id: str) -> Optional[Category]:
        raise NotImplementedError

    @abstractmethod
    async def find_by_name(self, name: CategoryName) -> Optional[Category]:
        raise NotImplementedError

    @abstractmethod
    async def find_all_active(self) -> List[Category]:
        """활성화된 모든 카테고리를 정렬순으로 조회"""
        raise NotImplementedError

    @abstractmethod
    async def find_all(
        self, page: int = 1, items_per_page: int = 10, include_inactive: bool = False
    ) -> Tuple[int, List[Category]]:
        """모든 카테고리 조회 (페이징)"""
        raise NotImplementedError

    @abstractmethod
    async def update(self, category: Category) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, category_id: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def exists_by_name(self, name: CategoryName) -> bool:
        """같은 이름의 카테고리가 이미 존재하는지 확인"""
        raise NotImplementedError
