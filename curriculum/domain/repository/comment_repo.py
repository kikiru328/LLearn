from abc import ABCMeta, abstractmethod
from typing import Optional, List, Tuple
from curriculum.domain.entity.comment import Comment


class ICommentRepository(metaclass=ABCMeta):
    @abstractmethod
    async def create(self, comment: Comment) -> None:
        raise NotImplementedError

    @abstractmethod
    async def find_by_id(self, comment_id: str) -> Optional[Comment]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, comment: Comment) -> None:
        raise NotImplementedError

    @abstractmethod
    async def soft_delete(self, comment_id: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def find_by_curriculum(
        self,
        curriculum_id: str,
        page: int = 1,
        items_per_page: int = 10,
        include_deleted: bool = False,
    ) -> Tuple[int, List[Comment]]:
        """커리큘럼의 댓글 목록 조회 (최상위 댓글만)"""
        raise NotImplementedError

    @abstractmethod
    async def find_replies_by_parent(
        self,
        parent_comment_id: str,
        page: int = 1,
        items_per_page: int = 10,
        include_deleted: bool = False,
    ) -> Tuple[int, List[Comment]]:
        """특정 댓글의 대댓글 목록 조회"""
        raise NotImplementedError

    @abstractmethod
    async def count_by_curriculum(
        self, curriculum_id: str, include_deleted: bool = False
    ) -> int:
        """커리큘럼의 총 댓글 수"""
        raise NotImplementedError

    @abstractmethod
    async def count_replies_by_parent(
        self, parent_comment_id: str, include_deleted: bool = False
    ) -> int:
        """특정 댓글의 대댓글 수"""
        raise NotImplementedError

    @abstractmethod
    async def find_by_user(
        self,
        user_id: str,
        page: int = 1,
        items_per_page: int = 10,
        include_deleted: bool = False,
    ) -> Tuple[int, List[Comment]]:
        """사용자가 작성한 댓글 목록"""
        raise NotImplementedError
