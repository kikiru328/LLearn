from typing import Optional, List, Tuple
from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from curriculum.domain.entity.comment import Comment
from curriculum.domain.repository.comment_repo import ICommentRepository
from curriculum.domain.value_object.comment_content import CommentContent
from curriculum.infra.db_models.comment import CommentModel


class CommentRepository(ICommentRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session: AsyncSession = session

    def _map_to_entity(self, comment_model: CommentModel) -> Comment:
        return Comment(
            id=comment_model.id,
            user_id=comment_model.user_id,
            curriculum_id=comment_model.curriculum_id,
            content=CommentContent(comment_model.content),
            parent_comment_id=comment_model.parent_comment_id,
            is_deleted=comment_model.is_deleted,
            created_at=comment_model.created_at,
            updated_at=comment_model.updated_at,
        )

    async def create(self, comment: Comment) -> None:
        new_comment = CommentModel(
            id=comment.id,
            user_id=comment.user_id,
            curriculum_id=comment.curriculum_id,
            content=comment.content.value,
            parent_comment_id=comment.parent_comment_id,
            is_deleted=comment.is_deleted,
            created_at=comment.created_at,
            updated_at=comment.updated_at,
        )
        self.session.add(new_comment)
        try:
            await self.session.commit()
        except:
            await self.session.rollback()
            raise

    async def find_by_id(self, comment_id: str) -> Optional[Comment]:
        query = select(CommentModel).where(CommentModel.id == comment_id)
        result = await self.session.execute(query)
        comment_model = result.scalar_one_or_none()

        if not comment_model:
            return None

        return self._map_to_entity(comment_model)

    async def update(self, comment: Comment) -> None:
        query = (
            update(CommentModel)
            .where(CommentModel.id == comment.id)
            .values(
                content=comment.content.value,
                is_deleted=comment.is_deleted,
                updated_at=comment.updated_at,
            )
        )
        await self.session.execute(query)
        try:
            await self.session.commit()
        except:
            await self.session.rollback()
            raise

    async def soft_delete(self, comment_id: str) -> None:
        from datetime import datetime, timezone

        query = (
            update(CommentModel)
            .where(CommentModel.id == comment_id)
            .values(
                is_deleted=True,
                updated_at=datetime.now(timezone.utc),
            )
        )
        await self.session.execute(query)
        try:
            await self.session.commit()
        except:
            await self.session.rollback()
            raise

    async def find_by_curriculum(
        self,
        curriculum_id: str,
        page: int = 1,
        items_per_page: int = 10,
        include_deleted: bool = False,
    ) -> Tuple[int, List[Comment]]:
        """최상위 댓글만 조회 (parent_comment_id가 None인 것들)"""
        base_query = select(CommentModel).where(
            CommentModel.curriculum_id == curriculum_id,
            CommentModel.parent_comment_id.is_(None),  # 최상위 댓글만
        )

        if not include_deleted:
            base_query = base_query.where(CommentModel.is_deleted == False)

        # 총 개수 조회
        count_query = select(func.count()).select_from(base_query.subquery())
        total_count = await self.session.scalar(count_query) or 0

        # 페이지네이션
        offset = (page - 1) * items_per_page
        paged_query = (
            base_query.limit(items_per_page)
            .offset(offset)
            .order_by(CommentModel.created_at.desc())
        )

        result = await self.session.execute(paged_query)
        comment_models = result.scalars().all()

        comments = [self._map_to_entity(model) for model in comment_models]
        return total_count, comments

    async def find_replies_by_parent(
        self,
        parent_comment_id: str,
        page: int = 1,
        items_per_page: int = 10,
        include_deleted: bool = False,
    ) -> Tuple[int, List[Comment]]:
        """특정 댓글의 대댓글 목록 조회"""
        base_query = select(CommentModel).where(
            CommentModel.parent_comment_id == parent_comment_id
        )

        if not include_deleted:
            base_query = base_query.where(CommentModel.is_deleted == False)

        # 총 개수 조회
        count_query = select(func.count()).select_from(base_query.subquery())
        total_count = await self.session.scalar(count_query) or 0

        # 페이지네이션
        offset = (page - 1) * items_per_page
        paged_query = (
            base_query.limit(items_per_page)
            .offset(offset)
            .order_by(CommentModel.created_at.asc())  # 대댓글은 오래된 순으로
        )

        result = await self.session.execute(paged_query)
        comment_models = result.scalars().all()

        comments = [self._map_to_entity(model) for model in comment_models]
        return total_count, comments

    async def count_by_curriculum(
        self, curriculum_id: str, include_deleted: bool = False
    ) -> int:
        """커리큘럼의 전체 댓글 수 (대댓글 포함)"""
        query = (
            select(func.count())
            .select_from(CommentModel)
            .where(CommentModel.curriculum_id == curriculum_id)
        )

        if not include_deleted:
            query = query.where(CommentModel.is_deleted == False)

        return await self.session.scalar(query) or 0

    async def count_replies_by_parent(
        self, parent_comment_id: str, include_deleted: bool = False
    ) -> int:
        """특정 댓글의 대댓글 수"""
        query = (
            select(func.count())
            .select_from(CommentModel)
            .where(CommentModel.parent_comment_id == parent_comment_id)
        )

        if not include_deleted:
            query = query.where(CommentModel.is_deleted == False)

        return await self.session.scalar(query) or 0

    async def find_by_user(
        self,
        user_id: str,
        page: int = 1,
        items_per_page: int = 10,
        include_deleted: bool = False,
    ) -> Tuple[int, List[Comment]]:
        """사용자가 작성한 댓글 목록"""
        base_query = select(CommentModel).where(CommentModel.user_id == user_id)

        if not include_deleted:
            base_query = base_query.where(CommentModel.is_deleted == False)

        # 총 개수 조회
        count_query = select(func.count()).select_from(base_query.subquery())
        total_count = await self.session.scalar(count_query) or 0

        # 페이지네이션
        offset = (page - 1) * items_per_page
        paged_query = (
            base_query.limit(items_per_page)
            .offset(offset)
            .order_by(CommentModel.created_at.desc())
        )

        result = await self.session.execute(paged_query)
        comment_models = result.scalars().all()

        comments = [self._map_to_entity(model) for model in comment_models]
        return total_count, comments
