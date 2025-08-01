from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from curriculum.domain.entity.feedback import Feedback
from curriculum.domain.repository.feedback_repo import IFeedbackRepository
from curriculum.domain.value_object.feedback_comment import FeedbackComment
from curriculum.domain.value_object.feedback_score import FeedbackScore
from curriculum.infra.db_models.feedback import FeedbackModel


class FeedbackRepository(IFeedbackRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session: AsyncSession = session

    async def create(self, feedback: Feedback) -> None:
        new = FeedbackModel(
            id=feedback.id,
            summary_id=feedback.summary_id,
            comment=feedback.comment.value,
            score=feedback.score.value,
            created_at=feedback.created_at,
            updated_at=feedback.updated_at,
        )
        self.session.add(new)
        try:
            await self.session.commit()
        except:
            await self.session.rollback()
            raise

    async def find_by_summary_id(self, summary_id: str) -> Optional[Feedback]:

        query = select(FeedbackModel).where(FeedbackModel.summary_id == summary_id)
        result = await self.session.execute(query)
        feedback_model = result.scalar_one_or_none()
        # model: FeedbackModel | None = await self.session.get(FeedbackModel, summary_id)
        if feedback_model is None:
            return None

        return Feedback(
            id=feedback_model.id,
            summary_id=feedback_model.summary_id,
            comment=FeedbackComment(feedback_model.comment),
            score=FeedbackScore(feedback_model.score),
            created_at=feedback_model.created_at,
            updated_at=feedback_model.updated_at,
        )

    async def delete(self, id: str) -> None:
        model: FeedbackModel | None = await self.session.get(FeedbackModel, id)
        if not model:
            return
        await self.session.delete(model)
        try:
            await self.session.commit()
        except:
            await self.session.rollback()
            raise
