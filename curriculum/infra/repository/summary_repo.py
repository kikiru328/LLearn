from datetime import datetime
from typing import List, cast
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from curriculum.infra.db_models.curriculum import SummaryModel
from curriculum.domain.entity.summary import Summary as SummaryEntity
from curriculum.domain.value_object.summary_content import SummaryContent


class SummaryRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def save(
        self,
        curriculum_id: str,
        week_number_vo,
        summary_entity: SummaryEntity,
    ) -> None:
        summary_model = SummaryModel(
            id=summary_entity.id,
            curriculum_id=curriculum_id,
            week_schedule_id=week_number_vo.value,
            content=str(summary_entity.content),
            submitted_at=summary_entity.submitted_at,
        )
        self._session.add(summary_model)
        await self._session.commit()

    async def find_by_week(
        self,
        curriculum_id: str,
        week_number_vo,
    ) -> List[SummaryEntity]:
        query = select(SummaryModel).where(
            SummaryModel.curriculum_id == curriculum_id,
            SummaryModel.week_schedule_id == week_number_vo.value,
        )
        result = await self._session.execute(query)
        summary_models = result.scalars().all()

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
