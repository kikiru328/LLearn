from typing import Optional, List
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.feedback import Feedback
from domain.repositories.feedback_repository import FeedbackRepository
from infrastructure.database.models.feedback_model import FeedbackModel


class FeedbackRepositoryImpl(FeedbackRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, feedback: Feedback) -> Feedback:
        feedback_model = FeedbackModel(
            id=str(feedback.id),
            summary_id=str(feedback.summary_id),
            content=feedback.content,
            created_at=feedback.created_at
        )
        self.session.add(feedback_model)
        await self.session.commit()
        await self.session.refresh(feedback_model)
        return self._model_to_entity(feedback_model=feedback_model)

    async def find_by_id(self, feedback_id: UUID) -> Optional[Feedback]:
        stmt = select(FeedbackModel).where(FeedbackModel.id==str(feedback_id))
        result = await self.session.execute(stmt)
        feedback_model = result.scalar_one_or_none()
        if feedback_model is None:
            return None
        return self._model_to_entity(feedback_model)

    async def find_by_summary_id(self, summary_id: UUID) -> Optional[Feedback]:
        stmt = select(FeedbackModel).where(FeedbackModel.summary_id==str(summary_id))
        result = await self.session.execute(stmt)
        feedback_model = result.scalar_one_or_none()
        if feedback_model is None:
            return None
        return self._model_to_entity(feedback_model)

    async def find_all(self) -> List[Feedback]:
        stmt = select(FeedbackModel)
        result = await self.session.execute(stmt)
        feedback_models = result.scalars().all()
        return [self._model_to_entity(model) for model in feedback_models]

    async def delete(self, feedback_id: UUID) -> bool:
        stmt = select(FeedbackModel).where(FeedbackModel.id==str(feedback_id))
        result = await self.session.execute(stmt)
        feedback_model = result.scalar_one_or_none()
        if feedback_model is None:
            return False
        await self.session.delete(feedback_model)
        await self.session.commit()
        return True


    def _model_to_entity(self, feedback_model: FeedbackModel) -> Feedback:
        return Feedback(
            id=UUID(feedback_model.id),
            summary_id=UUID(feedback_model.summary_id),
            content=feedback_model.content,
            created_at=feedback_model.created_at
        )