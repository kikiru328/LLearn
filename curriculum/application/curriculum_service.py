from datetime import datetime, timezone
from typing import List
from ulid import ULID
from curriculum.application.exception import (
    CurriculumNotFoundError,
    SummaryNotFoundError,
    WeekScheduleNotFoundError,
)
from curriculum.domain.entity.curriculum import Curriculum
from curriculum.domain.entity.feedback import Feedback
from curriculum.domain.entity.summary import Summary
from curriculum.domain.entity.week_schedule import WeekSchedule
from curriculum.domain.repository.curriculum_repo import ICurriculumRepository
from curriculum.domain.repository.feedback_repo import IFeedbackRepository
from curriculum.domain.repository.llm_client_repo import ILLMClient
from curriculum.domain.repository.summary_repo import ISummaryRepository
from curriculum.domain.value_object.feedback_comment import FeedbackComment
from curriculum.domain.value_object.feedback_score import FeedbackScore
from curriculum.domain.value_object.summary_content import SummaryContent
from curriculum.domain.value_object.title import Title
from curriculum.domain.value_object.topics import Topics
from curriculum.domain.value_object.week_number import WeekNumber


class CurriculumService:
    def __init__(
        self,
        curriculum_repo: ICurriculumRepository,
        summary_repo: ISummaryRepository,
        feedback_repo: IFeedbackRepository,
        llm_client: ILLMClient,
        ulid: ULID = ULID(),
    ) -> None:

        self.ulid = ulid
        self.curriculum_repo: ICurriculumRepository = curriculum_repo
        self.summary_repo = summary_repo
        self.feedback_repo = feedback_repo
        self.llm_client = llm_client

    # --------------------------
    # Curriculum Service: aggregate root
    # --------------------------

    async def create_curriculum(
        self,
        owner_id: str,
        title: str,
        week_schedules: List[WeekSchedule],
        created_at: datetime | None = None,
    ) -> Curriculum:
        created_at = created_at or datetime.now(timezone.utc)
        id = self.ulid.generate()  # new_id
        curriculum = Curriculum(
            id=id,
            owner_id=owner_id,
            title=Title(title),
            created_at=created_at,
            updated_at=created_at,
            week_schedules=week_schedules,
        )

        await self.curriculum_repo.save(curriculum)
        return curriculum

    async def generate_and_create_curriculum(
        self,
        owner_id: str,
        goal: str,
        weeks: int,
    ) -> Curriculum:

        raw = await self.llm_client.generate_schedule(goal, weeks)
        week_schedules: list[WeekSchedule] = []
        for item in raw:
            # MyPy가 object로 보는 값을 명시적 변환
            week_num = int(item["week_number"])
            topics_list = list(item["topics"])  # runtime엔 list[str]이어야 함
            week_schedules.append(
                WeekSchedule(
                    week_number=WeekNumber(week_num),
                    topics=Topics(topics_list),
                )
            )
        return await self.create_curriculum(owner_id, goal, week_schedules)

    async def get_curriculum_by_id(
        self,
        curriculum_id: str,
    ) -> Curriculum:
        existing_curriculum = await self.curriculum_repo.find_by_id(curriculum_id)
        if existing_curriculum is None:
            raise CurriculumNotFoundError(f"curriculum {curriculum_id} not found")
        return existing_curriculum

    async def get_curriculums(
        self,
        page: int,
        items_per_page: int,
    ) -> tuple[int, list[Curriculum]]:
        curriculums = await self.curriculum_repo.find_curriculums(page, items_per_page)
        return curriculums

    async def update_curriculum_title(
        self,
        curriculum_id: str,
        title: str,
    ):
        curriculum = await self.get_curriculum_by_id(curriculum_id)
        curriculum.title = Title(title)
        curriculum.updated_at = datetime.now(timezone.utc)

        await self.curriculum_repo.update(curriculum)
        return curriculum

    async def delete_curriculum(
        self,
        curriculum_id: str,
    ):
        existing = await self.curriculum_repo.find_by_id(curriculum_id)
        if existing is None:
            raise CurriculumNotFoundError(f"curriculum {curriculum_id} not found")

        await self.curriculum_repo.delete(curriculum_id)

    # --------------------------
    # Week Schedule Service: sub domain (root: curriculum)
    # --------------------------

    async def add_week_schedule(
        self,
        curriculum_id: str,
        week_number: int,
        topics: list[str],
    ):

        week_vo = WeekNumber(week_number)
        topics_vo = Topics(topics)
        curriculum = await self.get_curriculum_by_id(curriculum_id)

        new_schedule = WeekSchedule(
            week_number=week_vo,
            topics=topics_vo,
        )

        curriculum.week_schedules.append(new_schedule)

        await self.curriculum_repo.update(curriculum)

        return new_schedule

    async def get_week_schedule(
        self,
        curriculum_id: str,
        week_number: int,
    ) -> WeekSchedule:
        week_vo = WeekNumber(week_number)
        curriculum = await self.get_curriculum_by_id(curriculum_id)
        for schedule in curriculum.week_schedules:
            if schedule.week_number == week_vo:
                return schedule
        raise CurriculumNotFoundError(
            f"WeekSchedule for week {week_number} not found in curriculum {curriculum_id}"
        )

    async def get_list_week_schedules(
        self,
        curriculum_id: str,
    ) -> list[WeekSchedule]:
        curriculum = await self.get_curriculum_by_id(curriculum_id)
        return curriculum.week_schedules

    async def update_week_schedule(
        self,
        curriculum_id: str,
        week_number: int,
        topics: list,
    ) -> WeekSchedule:
        curriculum = await self.get_curriculum_by_id(curriculum_id)
        week_vo = WeekNumber(week_number)

        for schedule in curriculum.week_schedules:
            if schedule.week_number == week_vo:
                schedule.topics = Topics(topics)
                curriculum.updated_at = datetime.now(timezone.utc)
                await self.curriculum_repo.update(curriculum)
                return schedule
        raise WeekScheduleNotFoundError(
            f"WeekSchedule for week {week_number} not found in curriculum {curriculum_id}"
        )

    async def delete_week_schedule(
        self,
        curriculum_id: str,
        week_number: int,
    ):
        curriculum = await self.get_curriculum_by_id(curriculum_id)
        week_vo = WeekNumber(week_number)

        original_len = len(curriculum.week_schedules)
        curriculum.week_schedules = [
            ws for ws in curriculum.week_schedules if ws.week_number != week_vo
        ]
        if len(curriculum.week_schedules) == original_len:
            raise WeekScheduleNotFoundError(
                f"WeekSchedule for week {week_number} not found in curriculum {curriculum_id}"
            )
        await self.curriculum_repo.update(curriculum)

    # --------------------------
    # Summary Service: sub domain (root: curriculum)
    # --------------------------

    async def submit_summary(
        self,
        curriculum_id: str,
        week_number: int,
        content: SummaryContent,
        submitted_at: datetime | None = None,
    ):
        curriculum = await self.get_curriculum_by_id(curriculum_id)
        week_vo = WeekNumber(week_number)
        submitted_at = submitted_at or datetime.now(timezone.utc)
        summary = Summary(
            id=self.ulid.generate(), content=content, submitted_at=submitted_at
        )
        await self.summary_repo.save(
            curriculum.id,
            week_vo,
            summary,
        )
        return summary

    async def get_summaries_by_week(
        self,
        curriculum_id: str,
        week_number: int,
    ) -> list[Summary]:
        curriculum = await self.get_curriculum_by_id(curriculum_id)
        # VO 변환
        week_vo = WeekNumber(week_number)
        return await self.summary_repo.find_by_week(curriculum.id, week_vo)

    async def provide_feedback(
        self,
        curriculum_id: str,
        week_number: int,
        summary_id: str,
        comment: FeedbackComment,
        score: FeedbackScore,
    ) -> Feedback:
        # 1) 검증: curriculum exists
        await self.get_curriculum_by_id(curriculum_id)
        # 2) 검증: summary exists for given week
        week_vo = WeekNumber(week_number)
        summaries = await self.summary_repo.find_by_week(curriculum_id, week_vo)
        if not any(s.id == summary_id for s in summaries):
            raise SummaryNotFoundError(
                f"Summary {summary_id} not found in curriculum {curriculum_id} week {week_number}"
            )
        # 3) 생성 및 저장
        now = datetime.now(timezone.utc)
        feedback = Feedback(
            id=self.ulid.generate(), comment=comment, score=score, created_at=now
        )
        await self.feedback_repo.save(
            curriculum_id,
            week_vo,
            summary_id,
            feedback,
        )
        return feedback

    async def delete_summary(self, summary_id: str) -> None:
        # 1) cascade delete feedbacks
        await self.feedback_repo.delete_by_summary(summary_id)
        # 2) delete summary itself
        await self.summary_repo.delete(summary_id)

    # --------------------------
    # Feedback Service: sub domain (root: curriculum)
    # --------------------------

    async def get_feedbacks_by_week(
        self,
        curriculum_id: str,
        week_number: int,
    ) -> list[Feedback]:
        # 1) 커리큘럼 검증
        await self.get_curriculum_by_id(curriculum_id)
        # 2) VO 변환
        week_vo = WeekNumber(week_number)
        # 3) 조회
        return await self.feedback_repo.find_by_week(curriculum_id, week_vo)

    async def get_all_feedbacks(
        self,
        curriculum_id: str,
    ) -> list[Feedback]:
        # 1) 커리큘럼 검증
        await self.get_curriculum_by_id(curriculum_id)
        # 2) 전체 조회
        return await self.feedback_repo.find_all(curriculum_id)

    async def delete_feedbacks_by_summary(
        self,
        summary_id: str,
    ) -> None:
        # summary 존재 여부는 summary_repo로 검증해도 되고, 단순히 삭제만 해도 무방
        await self.feedback_repo.delete_by_summary(summary_id)
