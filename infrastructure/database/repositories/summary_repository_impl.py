from typing import Optional, List
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.summary import Summary
from domain.repositories.summary_repository import SummaryRepository
from infrastructure.database.models.summary_model import SummaryModel


class SummaryRepositoryImpl(SummaryRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, summary: Summary) -> Summary:
        summary_model = SummaryModel(
            id=str(summary.id),
            user_id=str(summary.user_id),
            week_topic_id=str(summary.week_topic_id),
            content=summary.content,
            is_public=summary.is_public,
            created_at=summary.created_at,
            updated_at=summary.updated_at
        )

        self.session.add(summary_model)
        await self.session.commit()
        await self.session.refresh(summary_model)
        return self._model_to_entity(summary_model)

    async def find_by_id(self, summary_id: UUID) -> Optional[Summary]:
        stmt = select(SummaryModel).where(SummaryModel.id==str(summary_id))
        result = await self.session.execute(stmt)
        summary_model = result.scalar_one_or_none()
        if summary_model is None:
            return None
        return self._model_to_entity(summary_model)

    async def find_by_user_id(self, user_id: UUID) -> List[Summary]:
        stmt = select(SummaryModel).where(SummaryModel.user_id==str(user_id))
        result = await self.session.execute(stmt)
        summary_models = result.scalars().all()
        return [self._model_to_entity(model) for model in summary_models]

    async def find_by_week_topic_id(self, week_topic_id: UUID) -> Optional[Summary]:
        stmt = select(SummaryModel).where(SummaryModel.week_topic_id==str(week_topic_id))
        result = await self.session.execute(stmt)
        summary_model = result.scalar_one_or_none()
        if summary_model is None:
            return None
        return self._model_to_entity(summary_model)
    
    async def find_by_week_topic_id_and_public(self, week_topic_id: UUID, is_public: bool) -> List[Summary]:
        """특정 주차의 공개/비공개 요약들 조회"""
        stmt = select(SummaryModel).where(
            SummaryModel.week_topic_id == str(week_topic_id),  # UUID → str 변환
            SummaryModel.is_public == is_public
        )
        result = await self.session.execute(stmt)
        summary_models = result.scalars().all()
        
        return [self._model_to_entity(model) for model in summary_models]
    
    async def find_public_summaries(self) -> List[Summary]:
        stmt = select(SummaryModel).where(SummaryModel.is_public == True)
        result = await self.session.execute(stmt)
        summary_models = result.scalars().all()
        return [self._model_to_entity(model) for model in summary_models]

    async def find_all(self) -> List[Summary]:
        stmt = select(SummaryModel)
        result = await self.session.execute(stmt)
        summary_models = result.scalars().all()
        return [self._model_to_entity(model) for model in summary_models]

    async def delete(self, summary_id: UUID) -> bool:
        stmt = select(SummaryModel).where(SummaryModel.id == str(summary_id))
        result = await self.session.execute(stmt)
        summary_model = result.scalar_one_or_none()
        if summary_model is None:
            return False

        await self.session.delete(summary_model)
        await self.session.commit()
        return True


    def _model_to_entity(self, summary_model: SummaryModel) -> Summary:
        return Summary(
            id=UUID(summary_model.id),
            user_id=UUID(summary_model.user_id),
            week_topic_id=UUID(summary_model.week_topic_id),
            content=summary_model.content,
            is_public=summary_model.is_public,
            created_at=summary_model.created_at,
            updated_at=summary_model.updated_at
        )