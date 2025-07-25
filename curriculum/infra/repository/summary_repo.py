from datetime import datetime
from typing import List, cast
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from curriculum.domain.value_object.week_number import WeekNumber
from curriculum.infra.db_models.curriculum import SummaryModel, WeekScheduleModel
from curriculum.domain.entity.summary import Summary as SummaryEntity
from curriculum.domain.value_object.summary_content import SummaryContent


class SummaryRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def save(
        self, curriculum_id: str, week_vo: WeekNumber, summary: SummaryEntity
    ) -> None:

        week_schedule_query = await self._session.execute(
            select(WeekScheduleModel.id).where(
                WeekScheduleModel.curriculum_id == curriculum_id,
                WeekScheduleModel.week_number == week_vo.value,
            )
        )
        week_schedule_id = week_schedule_query.scalar_one()

        summary_model = SummaryModel(
            id=summary.id,
            curriculum_id=curriculum_id,
            week_schedule_id=week_schedule_id,
            content=summary.content.value,
            submitted_at=summary.submitted_at,
        )
        self._session.add(summary_model)
        await self._session.commit()

    async def find_by_week(
        self, curriculum_id: str, week_vo: WeekNumber
    ) -> List[SummaryEntity]:
        week_schedule_query = await self._session.execute(
            select(WeekScheduleModel.id).where(
                WeekScheduleModel.curriculum_id == curriculum_id,
                WeekScheduleModel.week_number == week_vo.value,
            )
        )
        week_schedule_id = week_schedule_query.scalar_one()

        query_result = await self._session.execute(
            select(SummaryModel).where(
                SummaryModel.week_schedule_id == week_schedule_id
            )
        )
        summary_models = query_result.scalars().all()

        summaries: List[SummaryEntity] = []
        for summary_model in summary_models:
            submitted_at_dt: datetime = cast(datetime, summary_model.submitted_at)
            summaries.append(
                SummaryEntity(
                    id=summary_model.id,
                    content=SummaryContent(summary_model.content),
                    submitted_at=submitted_at_dt,
                )
            )
        return summaries

    async def delete(self, summary_id: str) -> None:
        delete_statement = delete(SummaryModel).where(SummaryModel.id == summary_id)
        await self._session.execute(delete_statement)
        await self._session.commit()
