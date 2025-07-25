# curriculum/infra/repository/feedback_repo_impl.py

from datetime import datetime
from typing import List, cast
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from curriculum.infra.db_models.curriculum import FeedbackModel
from curriculum.domain.entity.feedback import Feedback as FeedbackEntity
from curriculum.domain.value_object.feedback_comment import FeedbackComment
from curriculum.domain.value_object.feedback_score import FeedbackScore


class FeedbackRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def save(
        self,
        curriculum_id: str,
        week_number_vo,
        summary_id: str,
        feedback_entity: FeedbackEntity,
    ) -> None:
        feedback_model = FeedbackModel(
            id=feedback_entity.id,
            summary_id=summary_id,
            comment=feedback_entity.comment.value,
            score=feedback_entity.score.value,
            created_at=feedback_entity.created_at,
        )
        self._session.add(feedback_model)
        await self._session.commit()

    async def find_by_week(
        self,
        curriculum_id: str,
        week_number_vo,
    ) -> List[FeedbackEntity]:
        # curriculum_id, week_number not used directly, filtering happens via summary_id if needed
        query = select(FeedbackModel)
        result = await self._session.execute(query)
        feedback_models = result.scalars().all()

        feedbacks: List[FeedbackEntity] = []
        for feedback_model in feedback_models:
            # 명시적 캐스트
            created_at: datetime = cast(datetime, feedback_model.created_at)

            feedbacks.append(
                FeedbackEntity(
                    id=feedback_model.id,
                    comment=FeedbackComment(feedback_model.comment),
                    score=FeedbackScore(feedback_model.score),
                    created_at=created_at,
                )
            )
        return feedbacks

    async def find_all(
        self,
        curriculum_id: str,
    ) -> List[FeedbackEntity]:
        query = select(FeedbackModel)
        result = await self._session.execute(query)
        feedback_models = result.scalars().all()

        all_feedbacks: List[FeedbackEntity] = []
        for feedback_model in feedback_models:
            # 명시적 캐스트
            created_at_all: datetime = cast(datetime, feedback_model.created_at)

            all_feedbacks.append(
                FeedbackEntity(
                    id=feedback_model.id,
                    comment=FeedbackComment(feedback_model.comment),
                    score=FeedbackScore(feedback_model.score),
                    created_at=created_at_all,
                )
            )
        return all_feedbacks

    async def delete_by_summary(
        self,
        summary_id: str,
    ) -> None:
        delete_statement = delete(FeedbackModel).where(
            FeedbackModel.summary_id == summary_id
        )
        await self._session.execute(delete_statement)
        await self._session.commit()
