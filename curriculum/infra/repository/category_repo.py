from typing import Optional, List, Tuple
from sqlalchemy import func, select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from curriculum.domain.entity.category import Category
from curriculum.domain.repository.category_repo import ICategoryRepository
from curriculum.domain.value_object.category_name import CategoryName
from curriculum.infra.db_models.category import CategoryModel


class CategoryRepository(ICategoryRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session: AsyncSession = session

    def _map_to_entity(self, category_model: CategoryModel) -> Category:
        return Category(
            id=category_model.id,
            name=CategoryName(category_model.name),
            description=category_model.description,
            color=category_model.color,
            icon=category_model.icon,
            sort_order=category_model.sort_order,
            is_active=category_model.is_active,
            created_at=category_model.created_at,
            updated_at=category_model.updated_at,
        )

    async def create(self, category: Category) -> None:
        new_category = CategoryModel(
            id=category.id,
            name=category.name.value,
            description=category.description,
            color=category.color,
            icon=category.icon,
            sort_order=category.sort_order,
            is_active=category.is_active,
            created_at=category.created_at,
            updated_at=category.updated_at,
        )
        self.session.add(new_category)
        try:
            await self.session.commit()
        except:
            await self.session.rollback()
            raise

    async def find_by_id(self, category_id: str) -> Optional[Category]:
        query = select(CategoryModel).where(CategoryModel.id == category_id)
        result = await self.session.execute(query)
        category_model = result.scalar_one_or_none()

        if not category_model:
            return None

        return self._map_to_entity(category_model)

    async def find_by_name(self, name: CategoryName) -> Optional[Category]:
        query = select(CategoryModel).where(CategoryModel.name == name.value)
        result = await self.session.execute(query)
        category_model = result.scalar_one_or_none()

        if not category_model:
            return None

        return self._map_to_entity(category_model)

    async def find_all_active(self) -> List[Category]:
        query = (
            select(CategoryModel)
            .where(CategoryModel.is_active == True)
            .order_by(CategoryModel.sort_order.asc(), CategoryModel.name.asc())
        )

        result = await self.session.execute(query)
        category_models = result.scalars().all()

        return [self._map_to_entity(model) for model in category_models]

    async def find_all(
        self, page: int = 1, items_per_page: int = 10, include_inactive: bool = False
    ) -> Tuple[int, List[Category]]:
        base_query = select(CategoryModel)

        if not include_inactive:
            base_query = base_query.where(CategoryModel.is_active == True)

        # 총 개수 조회
        count_query = select(func.count()).select_from(base_query.subquery())
        total_count = await self.session.scalar(count_query) or 0

        # 페이지네이션
        offset = (page - 1) * items_per_page
        paged_query = (
            base_query.limit(items_per_page)
            .offset(offset)
            .order_by(CategoryModel.sort_order.asc(), CategoryModel.name.asc())
        )

        result = await self.session.execute(paged_query)
        category_models = result.scalars().all()

        categories = [self._map_to_entity(model) for model in category_models]
        return total_count, categories

    async def update(self, category: Category) -> None:
        existing_category = await self.session.get(CategoryModel, category.id)
        if not existing_category:
            raise ValueError(f"Category {category.id} not found")

        existing_category.name = category.name.value
        existing_category.description = category.description
        existing_category.color = category.color
        existing_category.icon = category.icon
        existing_category.sort_order = category.sort_order
        existing_category.is_active = category.is_active
        existing_category.updated_at = category.updated_at

        try:
            await self.session.commit()
        except:
            await self.session.rollback()
            raise

    async def delete(self, category_id: str) -> None:
        query = delete(CategoryModel).where(CategoryModel.id == category_id)
        await self.session.execute(query)
        try:
            await self.session.commit()
        except:
            await self.session.rollback()
            raise

    async def exists_by_name(self, name: CategoryName) -> bool:
        query = (
            select(func.count())
            .select_from(CategoryModel)
            .where(CategoryModel.name == name.value)
        )
        count = await self.session.scalar(query)
        return count > 0
