from typing import List, Optional, Tuple
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.selectable import Select
from curriculum.application.exception import SummaryNotFoundError
from curriculum.domain.entity.summary import Summary
from curriculum.domain.repository.summary_repo import ISummaryRepository
from curriculum.domain.value_object.summary_content import SummaryContent
from curriculum.domain.value_object.week_number import WeekNumber
from curriculum.infra.db_models.summary import SummaryModel


class SummaryRepository(ISummaryRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    def _map_model_to_entity(self, m: SummaryModel) -> Summary:
        return Summary(
            id=m.id,
            curriculum_id=m.curriculum_id,
            week_number=WeekNumber(m.week_number),
            content=SummaryContent(m.content),
            created_at=m.created_at,
            updated_at=m.updated_at,
        )

    async def create(self, summary: Summary) -> None:
        new_summary = SummaryModel(
            id=summary.id,
            curriculum_id=summary.curriculum_id,
            week_number=summary.week_number.value,
            content=summary.content.value,
            created_at=summary.created_at,
            updated_at=summary.updated_at,
        )
        self.session.add(new_summary)
        try:
            await self.session.commit()
        except:
            await self.session.rollback()
            raise

    async def delete(self, id: str) -> None:
        existing_summary: SummaryModel | None = await self.session.get(SummaryModel, id)
        if not existing_summary:
            raise SummaryNotFoundError(f"Summary with id={id} not found")
        await self.session.delete(existing_summary)
        try:
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise

    async def find_by_id(self, id: str) -> Optional[Summary]:
        existing_summary: SummaryModel | None = await self.session.get(SummaryModel, id)

        if not existing_summary:
            return None

        return Summary(
            id=existing_summary.id,
            curriculum_id=existing_summary.curriculum_id,
            week_number=WeekNumber(existing_summary.week_number),
            content=SummaryContent(existing_summary.content),
            created_at=existing_summary.created_at,
            updated_at=existing_summary.updated_at,
        )

    async def find_all_by_curriculum_and_week(
        self,
        curriculum_id: str,
        week_number: WeekNumber,
        page: int = 1,
        items_per_page: int = 10,
    ) -> Tuple[int, List[Summary]]:

        query: Select = (
            select(SummaryModel)
            .where(SummaryModel.curriculum_id == curriculum_id)
            .where(SummaryModel.week_number == week_number)
        )
        count_query = select(func.count()).select_from(query.subquery())
        total_count = await self.session.scalar(count_query)

        offset = (page - 1) * items_per_page
        paged = query.limit(items_per_page).offset(offset)
        response = await self.session.execute(paged)
        summaries = [
            self._map_model_to_entity(model) for model in response.scalars().all()
        ]

        return total_count, summaries

    async def find_all_by_curriculum(self, curriculum_id: str) -> List[Summary]:
        query: Select = (
            select(SummaryModel)
            .where(SummaryModel.curriculum_id == curriculum_id)
            .order_by(SummaryModel.week_number)
        )
        result = await self.session.execute(query)
        summary_models = result.scalars().all()
        return [
            Summary(
                id=summary_model.id,
                curriculum_id=summary_model.curriculum_id,
                week_number=WeekNumber(summary_model.week_number),
                content=SummaryContent(summary_model.content),
                created_at=summary_model.created_at,
                updated_at=summary_model.updated_at,
            )
            for summary_model in summary_models
        ]

    async def find_all_by_user(self, owner_id: str, page: int, items_per_page: int):
        query = (
            select(SummaryModel)
            .join(SummaryModel.curriculum)
            .where(SummaryModel.curriculum.has(user_id=owner_id))
            .order_by(SummaryModel.created_at.desc())
        )

        total_count = await self.session.scalar(
            select(func.count()).select_from(query.subquery())
        )
        offset = (page - 1) * items_per_page
        paged = query.limit(items_per_page).offset(offset)
        result = await self.session.execute(paged)
        summary_models = result.scalars().all()

        summaries = [
            Summary(
                id=summary_model.id,
                curriculum_id=summary_model.curriculum_id,
                week_number=WeekNumber(summary_model.week_number),
                content=SummaryContent(summary_model.content),
                created_at=summary_model.created_at,
                updated_at=summary_model.updated_at,
            )
            for summary_model in summary_models
        ]
        return total_count, summaries

    async def find_all_summaries_for_admin(
        self,
        page: int = 1,
        items_per_page: int = 10,
    ) -> Tuple[int, List[Summary]]:
        """관리자용 모든 요약 조회"""
        query = select(SummaryModel).order_by(SummaryModel.created_at.desc())

        count_query = select(func.count()).select_from(query.subquery())
        total_count = await self.session.scalar(count_query)

        offset = (page - 1) * items_per_page
        paged = query.limit(items_per_page).offset(offset)
        result = await self.session.execute(paged)
        summary_models = result.scalars().all()

        summaries = [self._map_model_to_entity(model) for model in summary_models]
        return total_count, summaries

    async def count_all_summaries(self) -> int:
        """전체 요약 수 조회"""
        query = select(func.count()).select_from(SummaryModel)
        return await self.session.scalar(query)
