from typing import Optional, List, Tuple
from sqlalchemy import func, select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from curriculum.domain.entity.like import Like
from curriculum.domain.repository.like_repo import ILikeRepository
from curriculum.infra.db_models.like import LikeModel


class LikeRepository(ILikeRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session: AsyncSession = session

    def _map_to_entity(self, like_model: LikeModel) -> Like:
        return Like(
            id=like_model.id,
            user_id=like_model.user_id,
            curriculum_id=like_model.curriculum_id,
            created_at=like_model.created_at,
        )

    async def create(self, like: Like) -> None:
        new_like = LikeModel(
            id=like.id,
            user_id=like.user_id,
            curriculum_id=like.curriculum_id,
            created_at=like.created_at,
        )
        self.session.add(new_like)
        try:
            await self.session.commit()
        except:
            await self.session.rollback()
            raise

    async def find_by_user_and_curriculum(
        self, user_id: str, curriculum_id: str
    ) -> Optional[Like]:
        query = select(LikeModel).where(
            LikeModel.user_id == user_id, LikeModel.curriculum_id == curriculum_id
        )
        result = await self.session.execute(query)
        like_model = result.scalar_one_or_none()

        if not like_model:
            return None

        return self._map_to_entity(like_model)

    async def delete_by_user_and_curriculum(
        self, user_id: str, curriculum_id: str
    ) -> None:
        query = delete(LikeModel).where(
            LikeModel.user_id == user_id, LikeModel.curriculum_id == curriculum_id
        )
        await self.session.execute(query)
        try:
            await self.session.commit()
        except:
            await self.session.rollback()
            raise

    async def count_by_curriculum(self, curriculum_id: str) -> int:
        query = (
            select(func.count())
            .select_from(LikeModel)
            .where(LikeModel.curriculum_id == curriculum_id)
        )
        return await self.session.scalar(query) or 0

    async def find_by_curriculum(
        self, curriculum_id: str, page: int = 1, items_per_page: int = 10
    ) -> Tuple[int, List[Like]]:
        query = select(LikeModel).where(LikeModel.curriculum_id == curriculum_id)

        count_query = select(func.count()).select_from(query.subquery())
        total_count = await self.session.scalar(count_query) or 0

        offset = (page - 1) * items_per_page
        paged_query = (
            query.limit(items_per_page)
            .offset(offset)
            .order_by(LikeModel.created_at.desc())
        )

        result = await self.session.execute(paged_query)
        like_models = result.scalars().all()

        likes = [self._map_to_entity(model) for model in like_models]
        return total_count, likes

    async def find_by_user(
        self, user_id: str, page: int = 1, items_per_page: int = 10
    ) -> Tuple[int, List[Like]]:
        query = select(LikeModel).where(LikeModel.user_id == user_id)

        count_query = select(func.count()).select_from(query.subquery())
        total_count = await self.session.scalar(count_query) or 0

        offset = (page - 1) * items_per_page
        paged_query = (
            query.limit(items_per_page)
            .offset(offset)
            .order_by(LikeModel.created_at.desc())
        )

        result = await self.session.execute(paged_query)
        like_models = result.scalars().all()

        likes = [self._map_to_entity(model) for model in like_models]
        return total_count, likes
