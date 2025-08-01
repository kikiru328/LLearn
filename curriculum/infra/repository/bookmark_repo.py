from typing import Optional, List, Tuple
from sqlalchemy import func, select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from curriculum.domain.entity.bookmark import Bookmark
from curriculum.domain.repository.bookmark_repo import IBookmarkRepository
from curriculum.infra.db_models.bookmark import BookmarkModel


class BookmarkRepository(IBookmarkRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session: AsyncSession = session

    def _map_to_entity(self, bookmark_model: BookmarkModel) -> Bookmark:
        return Bookmark(
            id=bookmark_model.id,
            user_id=bookmark_model.user_id,
            curriculum_id=bookmark_model.curriculum_id,
            created_at=bookmark_model.created_at,
        )

    async def create(self, bookmark: Bookmark) -> None:
        new_bookmark = BookmarkModel(
            id=bookmark.id,
            user_id=bookmark.user_id,
            curriculum_id=bookmark.curriculum_id,
            created_at=bookmark.created_at,
        )
        self.session.add(new_bookmark)
        try:
            await self.session.commit()
        except:
            await self.session.rollback()
            raise

    async def find_by_user_and_curriculum(
        self, user_id: str, curriculum_id: str
    ) -> Optional[Bookmark]:
        query = select(BookmarkModel).where(
            BookmarkModel.user_id == user_id,
            BookmarkModel.curriculum_id == curriculum_id,
        )
        result = await self.session.execute(query)
        bookmark_model = result.scalar_one_or_none()

        if not bookmark_model:
            return None

        return self._map_to_entity(bookmark_model)

    async def delete_by_user_and_curriculum(
        self, user_id: str, curriculum_id: str
    ) -> None:
        query = delete(BookmarkModel).where(
            BookmarkModel.user_id == user_id,
            BookmarkModel.curriculum_id == curriculum_id,
        )
        await self.session.execute(query)
        try:
            await self.session.commit()
        except:
            await self.session.rollback()
            raise

    async def find_by_user(
        self, user_id: str, page: int = 1, items_per_page: int = 10
    ) -> Tuple[int, List[Bookmark]]:
        query = select(BookmarkModel).where(BookmarkModel.user_id == user_id)

        count_query = select(func.count()).select_from(query.subquery())
        total_count = await self.session.scalar(count_query) or 0

        offset = (page - 1) * items_per_page
        paged_query = (
            query.limit(items_per_page)
            .offset(offset)
            .order_by(BookmarkModel.created_at.desc())
        )

        result = await self.session.execute(paged_query)
        bookmark_models = result.scalars().all()

        bookmarks = [self._map_to_entity(model) for model in bookmark_models]
        return total_count, bookmarks

    async def count_by_curriculum(self, curriculum_id: str) -> int:
        query = (
            select(func.count())
            .select_from(BookmarkModel)
            .where(BookmarkModel.curriculum_id == curriculum_id)
        )
        return await self.session.scalar(query) or 0
