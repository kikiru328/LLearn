from abc import ABCMeta, abstractmethod
from typing import Optional, List, Tuple
from curriculum.domain.entity.curriculum_tag import CurriculumTag, CurriculumCategory
from curriculum.domain.entity.tag import Tag
from curriculum.domain.entity.category import Category


class ICurriculumTagRepository(metaclass=ABCMeta):
    @abstractmethod
    async def create(self, curriculum_tag: CurriculumTag) -> None:
        raise NotImplementedError

    @abstractmethod
    async def find_by_curriculum_and_tag(
        self, curriculum_id: str, tag_id: str
    ) -> Optional[CurriculumTag]:
        raise NotImplementedError

    @abstractmethod
    async def find_tags_by_curriculum(self, curriculum_id: str) -> List[Tag]:
        """커리큘럼에 연결된 모든 태그 조회"""
        raise NotImplementedError

    @abstractmethod
    async def find_curriculums_by_tag(
        self, tag_id: str, page: int = 1, items_per_page: int = 10
    ) -> Tuple[int, List[str]]:
        """특정 태그가 연결된 커리큘럼 ID 목록 조회"""
        raise NotImplementedError

    @abstractmethod
    async def find_curriculums_by_tag_names(
        self, tag_names: List[str], page: int = 1, items_per_page: int = 10
    ) -> Tuple[int, List[str]]:
        """여러 태그 이름으로 커리큘럼 검색"""
        raise NotImplementedError

    @abstractmethod
    async def delete_by_curriculum_and_tag(
        self, curriculum_id: str, tag_id: str
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_all_by_curriculum(self, curriculum_id: str) -> None:
        """커리큘럼의 모든 태그 연결 삭제"""
        raise NotImplementedError

    @abstractmethod
    async def count_by_tag(self, tag_id: str) -> int:
        """특정 태그를 사용하는 커리큘럼 수"""
        raise NotImplementedError


class ICurriculumCategoryRepository(metaclass=ABCMeta):
    @abstractmethod
    async def create(self, curriculum_category: CurriculumCategory) -> None:
        raise NotImplementedError

    @abstractmethod
    async def find_by_curriculum_and_category(
        self, curriculum_id: str, category_id: str
    ) -> Optional[CurriculumCategory]:
        raise NotImplementedError

    @abstractmethod
    async def find_category_by_curriculum(
        self, curriculum_id: str
    ) -> Optional[Category]:
        """커리큘럼에 연결된 카테고리 조회 (하나만)"""
        raise NotImplementedError

    @abstractmethod
    async def find_curriculums_by_category(
        self, category_id: str, page: int = 1, items_per_page: int = 10
    ) -> Tuple[int, List[str]]:
        """특정 카테고리의 커리큘럼 ID 목록 조회"""
        raise NotImplementedError

    @abstractmethod
    async def update_curriculum_category(
        self, curriculum_id: str, new_category_id: str, assigned_by: str
    ) -> None:
        """커리큘럼의 카테고리 변경"""
        raise NotImplementedError

    @abstractmethod
    async def delete_by_curriculum(self, curriculum_id: str) -> None:
        """커리큘럼의 카테고리 연결 삭제"""
        raise NotImplementedError

    @abstractmethod
    async def count_by_category(self, category_id: str) -> int:
        """특정 카테고리를 사용하는 커리큘럼 수"""
        raise NotImplementedError
