from typing import Optional, List
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from domain.entities.week_topic import WeekTopic
from domain.repositories.week_topic_repository import WeekTopicRepository
from infrastructure.database.models.week_topic_model import WeekTopicModel


class WeekTopicRepositoryImpl(WeekTopicRepository):
    """WeekTopic Repository SQLAlchemy Implementation"""
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, week_topic: WeekTopic) -> WeekTopic:
        week_topic_model = WeekTopicModel(
            id=str(week_topic.id),
            curriculum_id=str(week_topic.curriculum_id),
            week_number=week_topic.week_number,
            title=week_topic.title,
            description=week_topic.description,
            learning_goals=week_topic.learning_goals,
            created_at=week_topic.created_at,
            updated_at=week_topic.updated_at
        )
        self.session.add(week_topic_model)
        await self.session.commit() #save
        await self.session.refresh(week_topic_model)

        return self._model_to_entity(week_topic_model=week_topic_model)

    async def find_by_id(self, week_topic_id: UUID) -> Optional[WeekTopic]:
        stmt = select(WeekTopicModel).where(WeekTopicModel.id==str(week_topic_id))
        result = await self.session.execute(stmt)
        week_topic_model = result.scalar_one_or_none()
        if week_topic_model is None:
            return None
        return self._model_to_entity(week_topic_model)

    async def find_by_curriculum_id(self, curriculum_id: UUID) -> List[WeekTopic]:
        stmt = select(WeekTopicModel).where(WeekTopicModel.curriculum_id==str(curriculum_id))
        result = await self.session.execute(stmt)
        week_topic_models = result.scalars().all()
        return [self._model_to_entity(model) for model in week_topic_models]

    async def find_by_curriculum_and_week(self, curriculum_id: UUID, week_number: int) -> Optional[WeekTopic]:
        stmt = select(WeekTopicModel).where(
            WeekTopicModel.curriculum_id==str(curriculum_id)
        ).where(WeekTopicModel.week_number==week_number)

        result = await self.session.execute(stmt)
        week_topic_model = result.scalar_one_or_none()
        if week_topic_model is None:
            return None
        return self._model_to_entity(week_topic_model)

    async def find_all(self) -> List[WeekTopic]:
        stmt = select(WeekTopicModel)
        result = await self.session.execute(stmt)
        week_topic_models = result.scalars().all()
        return [self._model_to_entity(model) for model in week_topic_models]

    async def delete(self, week_topic_id: UUID) -> bool:
        stmt = select(WeekTopicModel).where(WeekTopicModel.id==str(week_topic_id))
        result = await self.session.execute(stmt)
        week_topic_model = result.scalar_one_or_none()
        if week_topic_model is None:
            return False
        await self.session.delete(week_topic_model)
        await self.session.commit()
        return True

    def _model_to_entity(self, week_topic_model: WeekTopicModel) -> WeekTopic:
        return WeekTopic(
            id=UUID(week_topic_model.id),
            curriculum_id=UUID(week_topic_model.curriculum_id),
            week_number=week_topic_model.week_number,
            title=week_topic_model.title,
            description=week_topic_model.description,
            learning_goals=week_topic_model.learning_goals,
            created_at=week_topic_model.created_at,
            updated_at=week_topic_model.updated_at
        )
