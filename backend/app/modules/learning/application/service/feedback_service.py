from datetime import datetime, timezone
from typing import Any, Dict, Optional, List
from ulid import ULID  # type: ignore
from app.common.monitoring.metrics import increment_feedback_creation
from app.common.llm.llm_client_repo import ILLMClientRepository
from app.modules.curriculum.domain.entity.curriculum import Curriculum
from app.modules.curriculum.domain.entity.week_schedule import WeekSchedule
from app.modules.learning.application.dto.learning_dto import (
    CreateFeedbackCommand,
    UpdateFeedbackCommand,
    FeedbackDTO,
    FeedbackPageDTO,
    FeedbackQuery,
)
from app.modules.learning.application.exception import (
    FeedbackNotFoundError,
    FeedbackAlreadyExistsError,
    FeedbackAccessDeniedError,
    LLMFeedbackGenerationError,
)
from app.modules.learning.domain.entity.feedback import Feedback
from app.modules.learning.domain.entity.summary import Summary
from app.modules.learning.domain.repository.feedback_repo import IFeedbackRepository
from app.modules.learning.domain.repository.summary_repo import ISummaryRepository
from app.modules.learning.domain.service.learning_domain_service import (
    LearningDomainService,
)
from app.modules.curriculum.domain.repository.curriculum_repo import (
    ICurriculumRepository,
)
from app.modules.learning.domain.vo.feedback_comment import FeedbackComment
from app.modules.learning.domain.vo.feedback_score import FeedbackScore
from app.modules.user.domain.vo.role import RoleVO

from app.common.llm.decorators import trace_llm_operation

import logging

logger = logging.getLogger()


class FeedbackService:
    def __init__(
        self,
        feedback_repo: IFeedbackRepository,
        summary_repo: ISummaryRepository,
        curriculum_repo: ICurriculumRepository,
        learning_domain_service: LearningDomainService,
        llm_client: ILLMClientRepository,
        ulid: ULID = ULID(),
    ) -> None:
        self.feedback_repo: IFeedbackRepository = feedback_repo
        self.summary_repo: ISummaryRepository = summary_repo
        self.curriculum_repo: ICurriculumRepository = curriculum_repo
        self.learning_domain_service: LearningDomainService = learning_domain_service
        self.llm_client: ILLMClientRepository = llm_client
        self.ulid: ULID = ulid

    async def create_feedback(
        self,
        command: CreateFeedbackCommand,
        role: RoleVO,
    ) -> FeedbackDTO:
        """피드백 생성"""
        # 요약 존재 확인
        summary: Summary | None = await self.summary_repo.find_by_id(command.summary_id)
        if not summary:
            raise FeedbackNotFoundError(f"Summary {command.summary_id} not found")

        # 이미 피드백이 존재하는지 확인
        existing_feedback: Feedback | None = (
            await self.feedback_repo.find_by_summary_id(command.summary_id)
        )
        if existing_feedback:
            raise FeedbackAlreadyExistsError("Feedback already exists for this summary")

        # 접근 권한 확인
        can_access: bool = await self.learning_domain_service.can_access_summary(
            summary=summary,
            owner_id=command.owner_id,
            role=role,
        )

        if not can_access:
            raise FeedbackAccessDeniedError("Access denied to create feedback")

        feedback: Feedback = await self.learning_domain_service.create_feedback(
            feedback_id=self.ulid.generate(),
            summary_id=command.summary_id,
            comment=command.comment,
            score=command.score,
        )

        await self.feedback_repo.save(feedback)
        increment_feedback_creation()
        return FeedbackDTO.from_domain(feedback)

    @trace_llm_operation("generate_feedback")
    async def generate_feedback_with_llm(
        self,
        summary_id: str,
        user_id: str,
        role: RoleVO,
    ) -> FeedbackDTO:
        """LLM을 사용한 자동 피드백 생성"""
        # 요약 존재 확인
        summary: Summary | None = await self.summary_repo.find_by_id(summary_id)
        if not summary:
            raise FeedbackNotFoundError(f"Summary {summary_id} not found")

        # 이미 피드백이 존재하는지 확인
        existing_feedback: Feedback | None = (
            await self.feedback_repo.find_by_summary_id(summary_id)
        )
        if existing_feedback:
            raise FeedbackAlreadyExistsError("Feedback already exists for this summary")

        # 접근 권한 확인
        can_access: bool = await self.learning_domain_service.can_access_summary(
            summary=summary,
            owner_id=user_id,
            role=role,
        )

        if not can_access:
            raise FeedbackAccessDeniedError("Access denied to create feedback")

        # 커리큘럼과 주차 정보 조회
        curriculum: Curriculum | None = await self.curriculum_repo.find_by_id(
            curriculum_id=summary.curriculum_id,
            role=role,
            owner_id=user_id,
        )

        if not curriculum:
            raise FeedbackNotFoundError("Curriculum not found")

        # 해당 주차의 학습 내용 추출
        week_schedule: WeekSchedule | None = curriculum.get_week_schedule(
            summary.week_number
        )
        if not week_schedule:
            raise FeedbackNotFoundError(
                f"Week {summary.week_number.value} not found in curriculum"
            )

        lessons: List[str] = week_schedule.lessons.items

        try:
            # LLM을 통한 피드백 생성
            llm_response: Dict[str, Any] = await self.llm_client.generate_feedback(
                lessons=lessons,
                summary_content=summary.content.value,
            )

            # 5개 지표 점수 추출
            detailed_scores = {
                "cognitive_load_retention": llm_response.get(
                    "cognitive_load_retention", 0
                ),
                "engagement_behavior": llm_response.get("engagement_behavior", 0),
                "transfer_application": llm_response.get("transfer_application", 0),
                "competency_performance": llm_response.get("competency_performance", 0),
                "realtime_analytics": llm_response.get("realtime_analytics", 0),
            }
            feedback: Feedback = await self.learning_domain_service.create_feedback(
                feedback_id=self.ulid.generate(),
                summary_id=summary_id,
                comment=llm_response["comment"],
                score=llm_response["score"],
            )

            # 상세 점수 설정 (DB 저장 안함)
            feedback.set_detailed_scores(detailed_scores)

            # DTO에도 상세 점수 포함
            dto = FeedbackDTO.from_domain(feedback)
            dto.detailed_scores = detailed_scores

            await self.feedback_repo.save(feedback)
            increment_feedback_creation()

            return dto

        except Exception as e:
            logger.error(f"🔥 Feedback generation failed: {e}")
            raise LLMFeedbackGenerationError(f"Failed to generate feedback: {str(e)}")

    async def get_feedback_by_id(
        self,
        feedback_id: str,
        user_id: str,
        role: RoleVO,
    ) -> FeedbackDTO:
        """ID로 피드백 조회"""
        feedback: Feedback | None = await self.feedback_repo.find_by_id(feedback_id)
        if not feedback:
            raise FeedbackNotFoundError(f"Feedback {feedback_id} not found")

        # 접근 권한 확인
        can_access: bool = await self.learning_domain_service.can_access_feedback(
            feedback=feedback,
            user_id=user_id,
            role=role,
        )

        if not can_access:
            raise FeedbackAccessDeniedError("Access denied to feedback")

        return FeedbackDTO.from_domain(feedback)

    async def get_feedback_by_summary_id(
        self,
        summary_id: str,
        user_id: str,
        role: RoleVO,
    ) -> Optional[FeedbackDTO]:
        """요약 ID로 피드백 조회"""
        feedback: Feedback | None = await self.feedback_repo.find_by_summary_id(
            summary_id
        )
        if not feedback:
            return None

        # 접근 권한 확인
        can_access: bool = await self.learning_domain_service.can_access_feedback(
            feedback=feedback,
            user_id=user_id,
            role=role,
        )

        if not can_access:
            raise FeedbackAccessDeniedError("Access denied to feedback")

        return FeedbackDTO.from_domain(feedback)

    async def get_feedbacks(
        self,
        query: FeedbackQuery,
        user_id: str,
        role: RoleVO,
    ) -> FeedbackPageDTO:
        """피드백 목록 조회"""
        if query.curriculum_id:
            # 특정 커리큘럼의 모든 피드백들
            total_count, feedbacks = await self.feedback_repo.find_by_curriculum(
                curriculum_id=query.curriculum_id,
                page=query.page,
                items_per_page=query.items_per_page,
            )
        elif query.min_score is not None or query.max_score is not None:
            # 점수 범위로 피드백 조회
            min_score: float = query.min_score or 0.0
            max_score: float = query.max_score or 10.0
            total_count, feedbacks = await self.feedback_repo.find_by_score_range(
                min_score=min_score,
                max_score=max_score,
                page=query.page,
                items_per_page=query.items_per_page,
            )
        elif query.owner_id or role != RoleVO.ADMIN:
            # 사용자의 모든 피드백들
            owner_id: str = query.owner_id or user_id
            total_count, feedbacks = await self.feedback_repo.find_by_user(
                owner_id=owner_id,
                page=query.page,
                items_per_page=query.items_per_page,
            )
        else:
            # 관리자의 경우 모든 피드백 조회 (구현 필요시)
            total_count, feedbacks = await self.feedback_repo.find_by_user(
                owner_id=user_id,
                page=query.page,
                items_per_page=query.items_per_page,
            )

        # 접근 권한 필터링
        accessible_feedbacks = []
        for feedback in feedbacks:
            can_access = await self.learning_domain_service.can_access_feedback(
                feedback=feedback,
                user_id=user_id,
                role=role,
            )
            if can_access:
                accessible_feedbacks.append(feedback)

        return FeedbackPageDTO.from_domain(
            total_count=len(accessible_feedbacks),
            page=query.page,
            items_per_page=query.items_per_page,
            feedbacks=accessible_feedbacks,
        )

    async def update_feedback(
        self,
        command: UpdateFeedbackCommand,
        role: RoleVO,
    ) -> FeedbackDTO:
        """피드백 수정"""
        feedback: Feedback | None = await self.feedback_repo.find_by_id(
            command.feedback_id
        )
        if not feedback:
            raise FeedbackNotFoundError(f"Feedback {command.feedback_id} not found")

        # 수정 권한 확인
        can_modify: bool = await self.learning_domain_service.can_modify_feedback(
            feedback=feedback,
            user_id=command.owner_id,
            role=role,
        )

        if not can_modify:
            raise FeedbackAccessDeniedError("Access denied to modify feedback")

        feedback.update_feedback(
            new_comment=FeedbackComment(command.comment),
            new_score=FeedbackScore(command.score),
        )
        feedback.updated_at = datetime.now(timezone.utc)

        await self.feedback_repo.update(feedback)
        return FeedbackDTO.from_domain(feedback)

    async def delete_feedback(
        self,
        feedback_id: str,
        user_id: str,
        role: RoleVO,
    ) -> None:
        """피드백 삭제"""
        feedback: Feedback | None = await self.feedback_repo.find_by_id(feedback_id)
        if not feedback:
            raise FeedbackNotFoundError(f"Feedback {feedback_id} not found")

        # 삭제 권한 확인
        can_modify: bool = await self.learning_domain_service.can_modify_feedback(
            feedback=feedback,
            user_id=user_id,
            role=role,
        )

        if not can_modify:
            raise FeedbackAccessDeniedError("Access denied to delete feedback")

        await self.feedback_repo.delete(feedback_id)
