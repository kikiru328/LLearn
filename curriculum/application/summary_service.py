from datetime import datetime, timezone
from typing import List, Optional, Tuple
from ulid import ULID

from curriculum.domain.entity.feedback import Feedback
from curriculum.domain.entity.summary import Summary
from curriculum.domain.repository.curriculum_repo import ICurriculumRepository
from curriculum.domain.repository.feedback_repo import IFeedbackRepository
from curriculum.domain.repository.summary_repo import ISummaryRepository
from curriculum.domain.value_object.summary_content import SummaryContent
from curriculum.domain.value_object.week_number import WeekNumber
from curriculum.application.exception import (
    CurriculumNotFoundError,
    SummaryNotFoundError,
)
from user.domain.value_object.role import RoleVO


class SummaryService:
    def __init__(
        self,
        summary_repo: ISummaryRepository,
        curriculum_repo: ICurriculumRepository,
        feedback_repo: IFeedbackRepository,
        ulid: ULID = ULID(),
    ) -> None:

        self.summary_repo: ISummaryRepository = summary_repo
        self.curriculum_repo: ICurriculumRepository = curriculum_repo
        self.feedback_repo: IFeedbackRepository = feedback_repo
        self.ulid: ULID = ulid

    async def create_summary(
        self,
        owner_id: str,
        role: RoleVO,
        curriculum_id: str,
        week_number: int,
        content: str,
    ) -> Tuple[Summary, None]:

        curriculum = await self.curriculum_repo.find_by_id(
            id=curriculum_id,
            owner_id=owner_id,
            role=role,
        )

        if not curriculum:
            raise CurriculumNotFoundError(
                f"curriculum {curriculum_id} not found or access denied"
            )

        if role != RoleVO.ADMIN and curriculum.owner_id != owner_id:
            raise PermissionError("요약 생성 권한이 없습니다.")

        summary_content = SummaryContent(content)

        now = datetime.now(timezone.utc)
        summary_id = self.ulid.generate()
        summary = Summary(
            id=summary_id,
            curriculum_id=curriculum_id,
            week_number=WeekNumber(week_number),
            content=summary_content,
            created_at=now,
            updated_at=now,
        )

        await self.summary_repo.create(summary=summary)

        return summary, None  # sepearte feedback. no auto feedback

    async def get_summaries(
        self,
        owner_id: str,
        role: RoleVO,
        curriculum_id: str,
        week_number: int,
        page: int = 1,
        items_per_page: int = 10,
    ) -> Tuple[int, List[Summary]]:

        curriculum = await self.curriculum_repo.find_by_id(
            id=curriculum_id,
            owner_id=owner_id,
            role=role,
        )

        if not curriculum:
            raise CurriculumNotFoundError(
                f"curriculum {curriculum_id} not found or access denied"
            )

        total_count, summaries = (
            await self.summary_repo.find_all_by_curriculum_and_week(
                curriculum_id=curriculum_id,
                week_number=week_number,
                page=page,
                items_per_page=items_per_page,
            )
        )
        return total_count, summaries

    async def get_summary(
        self,
        owner_id: str,
        summary_id: str,
        role: RoleVO,
    ) -> Tuple[Summary, Optional[Feedback]]:

        summary = await self.summary_repo.find_by_id(summary_id)
        if not summary:
            raise SummaryNotFoundError(f"Summary {summary_id} not found")

        curriculum = await self.curriculum_repo.find_by_id(
            id=summary.curriculum_id,
            owner_id=owner_id,
            role=role,
        )
        if not curriculum:
            raise CurriculumNotFoundError(
                f"Curriculum {summary.curriculum_id} not found or access denied"
            )

        feedback = await self.feedback_repo.find_by_summary_id(summary_id)
        return summary, feedback

    async def delete_summary(
        self,
        owner_id: str,
        role: RoleVO,
        summary_id: str,
    ) -> None:

        summary = await self.summary_repo.find_by_id(summary_id)
        if not summary:
            raise SummaryNotFoundError(f"Summary {summary_id} not found")

        curriculum = await self.curriculum_repo.find_by_id(
            id=summary.curriculum_id,
            owner_id=owner_id,
            role=role,
        )
        if not curriculum:
            raise CurriculumNotFoundError(
                f"Curriculum {summary.curriculum_id} not found or access denied"
            )
        if role != RoleVO.ADMIN and curriculum.owner_id != owner_id:
            raise PermissionError("요약 삭제 권한이 없습니다")

        await self.summary_repo.delete(summary_id)

    async def get_my_summaries(
        self,
        owner_id: str,
        page: int = 1,
        items_per_page: int = 10,
    ):

        total_count, summaries = await self.summary_repo.find_all_by_user(
            owner_id=owner_id,
            page=page,
            items_per_page=items_per_page,
        )
        return total_count, summaries

    async def get_all_summaries_for_admin(
        self,
        page: int = 1,
        items_per_page: int = 10,
    ) -> Tuple[int, List[Summary]]:
        """관리자용 모든 요약 조회"""

        total_count, summaries = await self.summary_repo.find_all_summaries_for_admin(
            page=page,
            items_per_page=items_per_page,
        )
        return total_count, summaries

    async def get_summary_for_admin(
        self,
        summary_id: str,
    ) -> Tuple[Summary, Optional[Feedback]]:
        """관리자용 요약 상세 조회 (권한 체크 없음)"""

        summary = await self.summary_repo.find_by_id(summary_id)
        if not summary:
            raise SummaryNotFoundError(f"Summary {summary_id} not found")

        feedback = await self.feedback_repo.find_by_summary_id(summary_id)
        return summary, feedback

    async def delete_summary_for_admin(
        self,
        summary_id: str,
    ) -> None:
        """관리자용 요약 삭제 (권한 체크 없음)"""

        summary = await self.summary_repo.find_by_id(summary_id)
        if not summary:
            raise SummaryNotFoundError(f"Summary {summary_id} not found")

        await self.summary_repo.delete(summary_id)

    async def get_total_summaries_count(self) -> int:
        """전체 요약 수 조회 (Admin용)"""
        return await self.summary_repo.count_all_summaries()
