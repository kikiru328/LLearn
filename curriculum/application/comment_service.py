from datetime import datetime, timezone
from typing import List, Optional, Tuple
from ulid import ULID

from curriculum.application.exception import (
    CommentNotFoundError,
    CommentPermissionError,
    CurriculumNotFoundError,
)
from curriculum.domain.entity.comment import Comment
from curriculum.domain.repository.comment_repo import ICommentRepository
from curriculum.domain.repository.curriculum_repo import ICurriculumRepository
from curriculum.domain.value_object.comment_content import CommentContent
from user.domain.value_object.role import RoleVO
from monitoring.metrics import increment_comment


class CommentService:
    def __init__(
        self,
        comment_repo: ICommentRepository,
        curriculum_repo: ICurriculumRepository,
        ulid: ULID = ULID(),
    ) -> None:
        self.comment_repo: ICommentRepository = comment_repo
        self.curriculum_repo: ICurriculumRepository = curriculum_repo
        self.ulid: ULID = ulid

    async def create_comment(
        self,
        user_id: str,
        curriculum_id: str,
        content: str,
        parent_comment_id: Optional[str] = None,
        role: RoleVO = RoleVO.USER,
    ) -> Comment:
        """댓글 작성"""
        # 커리큘럼 존재 확인
        curriculum = await self.curriculum_repo.find_by_id(
            id=curriculum_id,
            role=role,
            owner_id=user_id if role != RoleVO.ADMIN else None,
        )
        if not curriculum:
            raise CurriculumNotFoundError(f"Curriculum {curriculum_id} not found")

        # 대댓글인 경우 부모 댓글 존재 확인
        if parent_comment_id:
            parent_comment = await self.comment_repo.find_by_id(parent_comment_id)
            if not parent_comment or parent_comment.is_deleted:
                raise CommentNotFoundError(
                    f"Parent comment {parent_comment_id} not found"
                )

            # 부모 댓글이 같은 커리큘럼의 댓글인지 확인
            if parent_comment.curriculum_id != curriculum_id:
                raise CommentPermissionError(
                    "Parent comment is not in the same curriculum"
                )

        now = datetime.now(timezone.utc)
        comment = Comment(
            id=self.ulid.generate(),
            user_id=user_id,
            curriculum_id=curriculum_id,
            content=CommentContent(content),
            parent_comment_id=parent_comment_id,
            is_deleted=False,
            created_at=now,
            updated_at=now,
        )

        await self.comment_repo.create(comment)

        increment_comment()

        return comment

    async def get_curriculum_comments(
        self,
        curriculum_id: str,
        user_id: str,
        role: RoleVO,
        page: int = 1,
        items_per_page: int = 10,
    ) -> Tuple[int, List[Comment]]:
        """커리큘럼의 댓글 목록 조회 (최상위 댓글만)"""
        # 커리큘럼 접근 권한 확인
        curriculum = await self.curriculum_repo.find_by_id(
            id=curriculum_id,
            role=role,
            owner_id=user_id if role != RoleVO.ADMIN else None,
        )
        if not curriculum:
            raise CurriculumNotFoundError(
                f"Curriculum {curriculum_id} not found or access denied"
            )

        return await self.comment_repo.find_by_curriculum(
            curriculum_id=curriculum_id,
            page=page,
            items_per_page=items_per_page,
            include_deleted=False,
        )

    async def get_comment_replies(
        self,
        parent_comment_id: str,
        user_id: str,
        role: RoleVO,
        page: int = 1,
        items_per_page: int = 10,
    ) -> Tuple[int, List[Comment]]:
        """댓글의 대댓글 목록 조회"""
        # 부모 댓글 존재 확인
        parent_comment = await self.comment_repo.find_by_id(parent_comment_id)
        if not parent_comment or parent_comment.is_deleted:
            raise CommentNotFoundError(f"Parent comment {parent_comment_id} not found")

        # 커리큘럼 접근 권한 확인
        curriculum = await self.curriculum_repo.find_by_id(
            id=parent_comment.curriculum_id,
            role=role,
            owner_id=user_id if role != RoleVO.ADMIN else None,
        )
        if not curriculum:
            raise CurriculumNotFoundError("Access denied to curriculum")

        return await self.comment_repo.find_replies_by_parent(
            parent_comment_id=parent_comment_id,
            page=page,
            items_per_page=items_per_page,
            include_deleted=False,
        )

    async def update_comment(
        self,
        comment_id: str,
        user_id: str,
        content: str,
        role: RoleVO = RoleVO.USER,
    ) -> Comment:
        """댓글 수정"""
        comment = await self.comment_repo.find_by_id(comment_id)
        if not comment or comment.is_deleted:
            raise CommentNotFoundError(f"Comment {comment_id} not found")

        # 권한 확인 (본인 댓글만 수정 가능, 관리자는 모든 댓글 수정 가능)
        if role != RoleVO.ADMIN and comment.user_id != user_id:
            raise CommentPermissionError("You can only edit your own comments")

        comment.content = CommentContent(content)
        comment.updated_at = datetime.now(timezone.utc)

        await self.comment_repo.update(comment)
        return comment

    async def delete_comment(
        self,
        comment_id: str,
        user_id: str,
        role: RoleVO = RoleVO.USER,
    ) -> None:
        """댓글 삭제 (소프트 삭제)"""
        comment = await self.comment_repo.find_by_id(comment_id)
        if not comment or comment.is_deleted:
            raise CommentNotFoundError(f"Comment {comment_id} not found")

        # 권한 확인 (본인 댓글만 삭제 가능, 관리자는 모든 댓글 삭제 가능)
        if role != RoleVO.ADMIN and comment.user_id != user_id:
            raise CommentPermissionError("You can only delete your own comments")

        await self.comment_repo.soft_delete(comment_id)

    async def get_user_comments(
        self,
        user_id: str,
        page: int = 1,
        items_per_page: int = 10,
    ) -> Tuple[int, List[Comment]]:
        """사용자가 작성한 댓글 목록"""
        return await self.comment_repo.find_by_user(
            user_id=user_id,
            page=page,
            items_per_page=items_per_page,
            include_deleted=False,
        )

    async def get_curriculum_comment_count(
        self,
        curriculum_id: str,
    ) -> int:
        """커리큘럼의 총 댓글 수"""
        return await self.comment_repo.count_by_curriculum(
            curriculum_id=curriculum_id,
            include_deleted=False,
        )

    async def get_comment_reply_count(
        self,
        parent_comment_id: str,
    ) -> int:
        """댓글의 대댓글 수"""
        return await self.comment_repo.count_replies_by_parent(
            parent_comment_id=parent_comment_id,
            include_deleted=False,
        )
