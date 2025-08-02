from datetime import datetime, timezone
from typing import Optional, List, Tuple
from sqlalchemy import func, select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from ulid import ULID

from curriculum.domain.entity.tag import Tag
from curriculum.domain.repository.tag_repo import ITagRepository
from curriculum.domain.value_object.tag_name import TagName
from curriculum.infra.db_models.tag import TagModel


class TagRepository(ITagRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session: AsyncSession = session

    def _map_to_entity(self, tag_model: TagModel) -> Tag:
        return Tag(
            id=tag_model.id,
            name=TagName(tag_model.name),
            usage_count=tag_model.usage_count,
            created_by=tag_model.created_by,
            created_at=tag_model.created_at,
            updated_at=tag_model.updated_at,
        )

    async def create(self, tag: Tag) -> None:
        new_tag = TagModel(
            id=tag.id,
            name=tag.name.value,
            usage_count=tag.usage_count,
            created_by=tag.created_by,
            created_at=tag.created_at,
            updated_at=tag.updated_at,
        )
        self.session.add(new_tag)
        try:
            await self.session.commit()
        except:
            await self.session.rollback()
            raise

    async def find_by_id(self, tag_id: str) -> Optional[Tag]:
        query = select(TagModel).where(TagModel.id == tag_id)
        result = await self.session.execute(query)
        tag_model = result.scalar_one_or_none()

        if not tag_model:
            return None

        return self._map_to_entity(tag_model)

    async def find_by_name(self, name: TagName) -> Optional[Tag]:
        query = select(TagModel).where(TagModel.name == name.value)
        result = await self.session.execute(query)
        tag_model = result.scalar_one_or_none()

        if not tag_model:
            return None

        return self._map_to_entity(tag_model)

    async def find_or_create_by_names(
        self, tag_names: List[TagName], created_by: str
    ) -> List[Tag]:
        """태그 이름 리스트로 태그들을 찾거나 생성"""
        tags = []
        now = datetime.now(timezone.utc)

        for tag_name in tag_names:
            # 기존 태그 찾기
            existing_tag = await self.find_by_name(tag_name)

            if existing_tag:
                tags.append(existing_tag)
            else:
                # 새 태그 생성
                new_tag = Tag(
                    id=ULID().generate(),
                    name=tag_name,
                    usage_count=0,
                    created_by=created_by,
                    created_at=now,
                    updated_at=now,
                )
                await self.create(new_tag)
                tags.append(new_tag)

        return tags

    async def find_popular_tags(self, limit: int = 20, min_usage: int = 1) -> List[Tag]:
        query = (
            select(TagModel)
            .where(TagModel.usage_count >= min_usage)
            .order_by(TagModel.usage_count.desc())
            .limit(limit)
        )

        result = await self.session.execute(query)
        tag_models = result.scalars().all()

        return [self._map_to_entity(model) for model in tag_models]

    async def search_by_name(self, query: str, limit: int = 10) -> List[Tag]:
        search_query = (
            select(TagModel)
            .where(TagModel.name.like(f"%{query.lower()}%"))
            .order_by(TagModel.usage_count.desc())
            .limit(limit)
        )

        result = await self.session.execute(search_query)
        tag_models = result.scalars().all()

        return [self._map_to_entity(model) for model in tag_models]

    async def find_all(
        self, page: int = 1, items_per_page: int = 20
    ) -> Tuple[int, List[Tag]]:
        base_query = select(TagModel)

        # 총 개수 조회
        count_query = select(func.count()).select_from(base_query.subquery())
        total_count = await self.session.scalar(count_query) or 0

        # 페이지네이션
        offset = (page - 1) * items_per_page
        paged_query = (
            base_query.limit(items_per_page)
            .offset(offset)
            .order_by(TagModel.usage_count.desc(), TagModel.name.asc())
        )

        result = await self.session.execute(paged_query)
        tag_models = result.scalars().all()

        tags = [self._map_to_entity(model) for model in tag_models]
        return total_count, tags

    async def update(self, tag: Tag) -> None:
        existing_tag = await self.session.get(TagModel, tag.id)
        if not existing_tag:
            raise ValueError(f"Tag {tag.id} not found")

        existing_tag.name = tag.name.value
        existing_tag.usage_count = tag.usage_count
        existing_tag.updated_at = tag.updated_at

        try:
            await self.session.commit()
        except:
            await self.session.rollback()
            raise

    async def delete(self, tag_id: str) -> None:
        query = delete(TagModel).where(TagModel.id == tag_id)
        await self.session.execute(query)
        try:
            await self.session.commit()
        except:
            await self.session.rollback()
            raise

    async def increment_usage_count(self, tag_id: str) -> None:
        query = (
            update(TagModel)
            .where(TagModel.id == tag_id)
            .values(
                usage_count=TagModel.usage_count + 1,
                updated_at=datetime.now(timezone.utc),
            )
        )
        await self.session.execute(query)
        try:
            await self.session.commit()
        except:
            await self.session.rollback()
            raise

    async def decrement_usage_count(self, tag_id: str) -> None:
        query = (
            update(TagModel)
            .where(TagModel.id == tag_id)
            .values(
                usage_count=func.greatest(
                    TagModel.usage_count - 1, 0
                ),  # 0 이하로 내려가지 않음
                updated_at=datetime.now(timezone.utc),
            )
        )
        await self.session.execute(query)
        try:
            await self.session.commit()
        except:
            await self.session.rollback()
            raise
