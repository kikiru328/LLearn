from datetime import datetime, timezone
from typing import List, Optional, Tuple
from ulid import ULID
from curriculum.application.exception import CurriculumNotFoundError
from curriculum.application.exception import (
    FeedbackAlreadyExistsError,
    FeedbackNotFoundError,
    SummaryNotFoundError,
)
from curriculum.domain.entity.feedback import Feedback
from curriculum.domain.repository.curriculum_repo import ICurriculumRepository
from curriculum.domain.repository.feedback_repo import IFeedbackRepository
from curriculum.domain.repository.summary_repo import ISummaryRepository
from curriculum.domain.value_object.feedback_comment import FeedbackComment
from curriculum.domain.value_object.feedback_score import FeedbackScore
from curriculum.infra.llm.I_llm_client_repo import ILLMClientRepository
from user.domain.value_object.role import RoleVO
from monitoring.metrics import increment_feedback_created


class FeedbackService:
    def __init__(
        self,
        feedback_repo: IFeedbackRepository,
        summary_repo: ISummaryRepository,
        curriculum_repo: ICurriculumRepository,
        llm_client: ILLMClientRepository,
        ulid: ULID = ULID(),
    ):

        self.feedback_repo: IFeedbackRepository = feedback_repo
        self.summary_repo: ISummaryRepository = summary_repo
        self.curriculum_repo: ICurriculumRepository = curriculum_repo
        self.llm_client: ILLMClientRepository = llm_client
        self.ulid: ULID = ulid

    async def create_feedback(
        self,
        owner_id: str,
        role: RoleVO,
        curriculum_id: str,
        summary_id: str,
    ) -> Feedback:

        summary = await self.summary_repo.find_by_id(id=summary_id)
        if not summary:
            raise SummaryNotFoundError(f"Summary {summary_id} not found")

        curriculum = await self.curriculum_repo.find_by_id(
            id=curriculum_id,
            owner_id=owner_id,
            role=role,
        )
        if not curriculum:
            raise PermissionError("이 커리큘럼에 대한 접근 권한이 없습니다.")

        existing_feedback = await self.feedback_repo.find_by_summary_id(summary_id)
        if existing_feedback:
            raise FeedbackAlreadyExistsError("이미 생성된 피드백이 있습니다.")

        lessons = [
            lesson
            for week_schedule in curriculum.week_schedules
            if week_schedule.week_number.value == summary.week_number.value
            for lesson in week_schedule.lessons.items
        ]
        llm_out = await self.llm_client.generate_feedback(
            lessons=lessons,
            summary_content=summary.content.value,
        )
        comment = FeedbackComment(llm_out["comment"])
        score = FeedbackScore(llm_out["score"])

        now = datetime.now(timezone.utc)
        feedback = Feedback(
            id=self.ulid.generate(),
            summary_id=summary_id,
            comment=comment,
            score=score,
            created_at=now,
            updated_at=now,
        )
        await self.feedback_repo.create(feedback)

        increment_feedback_created()

        return feedback

    async def get_feedback(
        self,
        owner_id: str,
        role: RoleVO,
        curriculum_id: str,
        summary_id: str,
    ) -> Optional[Feedback]:

        summary = await self.summary_repo.find_by_id(summary_id)
        if not summary:
            raise SummaryNotFoundError("Summary Not Found")

        curriculum = await self.curriculum_repo.find_by_id(
            id=curriculum_id,
            owner_id=owner_id,
            role=role,
        )
        if not curriculum:
            raise CurriculumNotFoundError("Curriculum Not Found or no Authenticated")

        feedback = await self.feedback_repo.find_by_summary_id(summary_id=summary_id)
        if not feedback:
            raise FeedbackNotFoundError("Feedback not found")
        return feedback

    async def delete_feedback(
        self,
        owner_id: str,
        role: RoleVO,
        curriculum_id: str,
        summary_id: str,
        feedback_id: str,
    ):

        summary = await self.summary_repo.find_by_id(summary_id)
        if not summary:
            raise SummaryNotFoundError(f"Summary {summary_id} not found")

        curriculum = await self.curriculum_repo.find_by_id(
            id=curriculum_id,
            owner_id=owner_id,
            role=role,
        )
        if not curriculum:
            raise CurriculumNotFoundError("커리큘럼을 찾을 수 없습니다.")

        feedback = await self.feedback_repo.find_by_summary_id(summary_id)
        if not feedback or feedback.summary_id != summary_id:
            raise FeedbackNotFoundError(f"Feedback {feedback_id} not found")

        if role != RoleVO.ADMIN and curriculum.owner_id != owner_id:
            raise PermissionError("피드백 삭제 권한이 없습니다")

        await self.feedback_repo.delete(feedback_id)

    async def get_all_feedbacks_for_admin(
        self,
        page: int = 1,
        items_per_page: int = 10,
    ) -> Tuple[int, List[Feedback]]:
        """관리자용 모든 피드백 조회"""

        total_count, feedbacks = await self.feedback_repo.find_all_feedbacks_for_admin(
            page=page,
            items_per_page=items_per_page,
        )
        return total_count, feedbacks

    async def delete_feedback_for_admin(
        self,
        feedback_id: str,
    ) -> None:
        """관리자용 피드백 삭제 (권한 체크 없음)"""

        await self.feedback_repo.delete(feedback_id)

    async def get_total_feedbacks_count(self) -> int:
        """전체 피드백 수 조회"""

        return await self.feedback_repo.count_all()

    async def delete_feedback_by_admin(self, feedback_id: str) -> None:
        """관리자용 피드백 삭제 (권한 체크 없음)"""
        await self.feedback_repo.delete(feedback_id)
