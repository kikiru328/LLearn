from datetime import datetime, timezone
import json
import re
from typing import List, Optional, Tuple
from zoneinfo import ZoneInfo
from ulid import ULID

from monitoring.metrics import (
    track_llm_metrics,
    increment_curriculum_created,
    track_db_metrics,
)

from curriculum.application.exception import (
    CurriculumCountOverError,
    CurriculumNotFoundError,
    WeekScheduleNotFoundError,
    WeekIndexOutOfRangeError,
)
from curriculum.application.prompt_templates import GEN_CURRICULUM_PROMPT
from curriculum.domain.entity.curriculum import Curriculum
from curriculum.domain.entity.week_schedule import WeekSchedule
from curriculum.domain.repository.curriculum_repo import ICurriculumRepository
from curriculum.domain.value_object.lessons import Lessons
from curriculum.domain.value_object.title import Title
from curriculum.domain.value_object.visibility import Visibility
from curriculum.domain.value_object.week_number import WeekNumber
from curriculum.infra.llm.I_llm_client_repo import ILLMClientRepository
from user.domain.value_object.role import RoleVO


class CurriculumService:
    def __init__(
        self,
        curriculum_repo: ICurriculumRepository,
        llm_client: ILLMClientRepository,
        ulid: ULID = ULID(),
    ) -> None:
        self.curriculum_repo: ICurriculumRepository = curriculum_repo
        self.llm_client: ILLMClientRepository = llm_client
        self.ulid: ULID = ulid

    @track_db_metrics("create", "curriculum")
    async def create_curriculum(
        self,
        owner_id: str,
        title: str,
        week_schedules: List[Tuple[int, List[str]]],
        visibility: Visibility = Visibility.PRIVATE,
    ) -> Curriculum:
        """
        수동으로 커리큘럼 생성, 10개 고정, 가장 오래된거 삭제
        """

        count = await self.curriculum_repo.count_owner(owner_id)
        if count >= 10:
            raise CurriculumCountOverError(
                "You can only have up to 10 curriculums. Delete one before creating a new one."
            )

        created_at: datetime = datetime.now(timezone.utc)
        new_id: str = self.ulid.generate()
        new_curriculum = Curriculum(
            id=new_id,
            owner_id=owner_id,
            title=Title(title),
            visibility=visibility,
            created_at=created_at,
            updated_at=created_at,
            week_schedules=[
                WeekSchedule(
                    week_number=WeekNumber(week_number), lessons=Lessons(lessons)
                )
                for week_number, lessons in week_schedules
            ],
        )
        await self.curriculum_repo.create(new_curriculum)

        increment_curriculum_created("manual")

        return new_curriculum

    @track_llm_metrics("curriculum_generation")
    @track_db_metrics("create", "curriculum")
    async def generate_curriculum(
        self,
        owner_id: str,
        goal: str,
        period_weeks: int,
        difficulty: str,
        details: str,
    ) -> Curriculum:
        prompt = GEN_CURRICULUM_PROMPT.format(
            goal=goal, period=period_weeks, difficulty=difficulty, details=details
        )
        raw: str = await self.llm_client.generate(prompt)

        def _strip_markdown_fences(text: str) -> str:
            """
            ``` 또는 ```json 같은 마크다운 펜스를 제거하고,
            앞뒤 공백/줄바꿈을 없앤 순수 JSON 문자열을 반환.
            """
            # 1) ```json\n 또는 ```\n 식의 펜스 제거
            without_fences = re.sub(r"```(?:json)?\s*\n?", "", text)
            # 2) 남아있는 ``` 제거
            without_fences = without_fences.replace("```", "")
            # 3) 앞뒤 공백·줄바꿈 트리밍
            return without_fences.strip()

        clean = _strip_markdown_fences(raw)

        if not raw:
            raise RuntimeError("LLM이 빈 문자열을 반환했습니다")

        try:
            parsed = json.loads(clean)
        except json.JSONDecodeError:
            raise RuntimeError("LLM 응답 파싱 실패")

        # ─── 1) parsed 타입 분기 ─────────────────────────────
        if isinstance(parsed, dict):
            title_str = parsed.get("title", "")
            schedule_list = parsed.get("schedule", [])

        elif isinstance(parsed, list):
            first = parsed[0] if parsed else {}
            if isinstance(first, dict) and "schedule" in first:
                title_str = first.get("title", "") or goal
                schedule_list = first.get("schedule", [])
            else:
                # B) 이전 버전: [{week_number:…, lessons:[…]}, …] 형태
                title_str = goal
                schedule_list = parsed  # parsed 자체가 스케줄 배열
        else:
            raise RuntimeError("LLM 응답 형식이 올바르지 않습니다")

        # ─── 2) Title VO 생성 ───────────────────────────────
        seoul_now = datetime.now(ZoneInfo("Asia/Seoul"))
        prefix = seoul_now.strftime("%y%m%d%H%M")
        # LLM이 뱉은 title_str 앞에 붙이기
        full_title = f"{prefix} {title_str}"
        title_vo = Title(full_title)

        # ─── 3) schedule → domain 포맷 변환 ─────────────────
        now = datetime.now(timezone.utc)
        curriculum_id = self.ulid.generate()
        weeks: list[tuple[int, list[str]]] = []
        for item in schedule_list:
            num = item.get("week_number") or item.get("weekNumber")
            lessons_raw = item.get("lessons") or item.get("topics")
            if num is None or lessons_raw is None:
                raise RuntimeError(f"Invalid schedule item: {item!r}")
            wn = WeekNumber(num)
            ls = Lessons(lessons_raw)
            weeks.append((wn.value, ls.items))

        curriculum = Curriculum(
            id=curriculum_id,
            owner_id=owner_id,
            title=title_vo,
            visibility=Visibility.PRIVATE,
            created_at=now,
            updated_at=now,
            week_schedules=[
                WeekSchedule(WeekNumber(week), Lessons(lesson))
                for week, lesson in weeks
            ],
        )
        await self.curriculum_repo.create(curriculum)

        increment_curriculum_created("generated")

        return curriculum

    async def get_curriculums(
        self,
        owner_id: str,
        role: RoleVO,
        page: int = 1,
        items_per_page: int = 10,
    ):
        total_count, curriculums = await self.curriculum_repo.find_curriculums(
            page=page,
            items_per_page=items_per_page,
            owner_id=owner_id,
            role=role,
        )
        return total_count, curriculums

    async def get_curriculum_by_id(
        self,
        curriculum_id: str,
        owner_id: str,
        role: RoleVO,
    ):
        curriculum = await self.curriculum_repo.find_by_id(
            id=curriculum_id,
            role=role,
            owner_id=owner_id,
        )
        if curriculum is None:
            raise CurriculumNotFoundError(f"Curriculum {curriculum_id} not found")
        return curriculum

    async def get_curriculum_by_title(
        self,
        title: str,
        user_id: str,
    ):
        curriculum = await self.curriculum_repo.find_by_title(
            title=title,
            owner_id=user_id,
        )
        if curriculum is None:
            raise CurriculumNotFoundError(f"{title} curriculum not found")
        return curriculum

    async def update_curriculum(
        self,
        curriculum_id: str,
        owner_id: str,
        role: RoleVO,
        title: Optional[str] = None,
        visibility: Optional[Visibility] = None,
    ) -> Curriculum:

        curriculum: Curriculum | None = await self.curriculum_repo.find_by_id(
            id=curriculum_id,
            owner_id=owner_id,
            role=role,
        )

        if curriculum is None:
            raise CurriculumNotFoundError(f"Curriculum with id={id} not found")

        if title:
            curriculum.title = Title(title)

        if visibility:
            curriculum.visibility = visibility

        curriculum.updated_at = datetime.now(timezone.utc)

        await self.curriculum_repo.update(curriculum)
        return curriculum

    async def delete_curriculum(self, id: str, owner_id: str, role: RoleVO) -> None:
        curriculum: Curriculum | None = await self.curriculum_repo.find_by_id(
            id=id,
            owner_id=owner_id,
            role=role,
        )

        if curriculum is None:
            raise CurriculumNotFoundError(f"Curriculum with id={id} not found")

        if role != RoleVO.ADMIN and curriculum.owner_id != owner_id:
            raise PermissionError("You are not allowed to delete this curriculum.")

        await self.curriculum_repo.delete(id)

    async def create_week_schedule(
        self,
        curriculum_id: str,
        owner_id: str,
        role: RoleVO,
        week_number: int,
        lessons: list[str],
    ):
        curriculum = await self.curriculum_repo.find_by_id(
            id=curriculum_id,
            owner_id=owner_id,
            role=role,
        )
        if not curriculum:
            raise CurriculumNotFoundError(f"curriculum {curriculum_id} not found")

        if role != RoleVO.ADMIN and curriculum.owner_id != owner_id:
            raise PermissionError("권한이 없습니다.")

        lessons_vo = Lessons(lessons)

        await self.curriculum_repo.insert_week_and_shift(
            curriculum_id=curriculum_id,
            new_week_number=week_number,
            lessons=lessons_vo.items,
        )

        updated = await self.curriculum_repo.find_by_id(
            id=curriculum_id,
            owner_id=owner_id,
            role=role,
        )
        if not updated:
            raise CurriculumNotFoundError(
                f"curriculum {curriculum_id} not found after insert"
            )

        return updated

    async def delete_week(
        self,
        curriculum_id: str,
        owner_id: str,
        role: RoleVO,
        week_number: int,
    ):

        curriculum = await self.curriculum_repo.find_by_id(
            id=curriculum_id,
            owner_id=owner_id,
            role=role,
        )

        if not curriculum:
            raise CurriculumNotFoundError(f"Curriculum with id={id} not found")

        if not any(
            week.week_number.value == week_number for week in curriculum.week_schedules
        ):
            raise WeekScheduleNotFoundError(...)

        await self.curriculum_repo.delete_week_and_shift(
            curriculum_id=curriculum_id,
            week_number=week_number,
        )

    async def create_lesson(
        self,
        curriculum_id: str,
        owner_id: str,
        role: RoleVO,
        week_number: int,
        lesson: str,
        lesson_index: int | None = None,
    ):
        curriculum = await self.curriculum_repo.find_by_id(
            id=curriculum_id,
            role=role,
            owner_id=owner_id,
        )
        if not curriculum:
            raise CurriculumNotFoundError(f"curriculum {curriculum_id} not found")

        if role != RoleVO.ADMIN and curriculum.owner_id != owner_id:
            raise PermissionError("권한이 없습니다")

        week_schedule = next(
            (
                week
                for week in curriculum.week_schedules
                if week.week_number.value == week_number
            ),
            None,
        )
        if not week_schedule:
            raise WeekScheduleNotFoundError(f"Week {week_number} not found")

        lessons = week_schedule.lessons.items
        max_index = len(lessons)
        insert_index = lesson_index if lesson_index is not None else max_index

        if not (0 <= insert_index <= max_index):
            raise WeekIndexOutOfRangeError("lesson_index out of range")

        lessons.insert(insert_index, lesson)

        await self.curriculum_repo.insert_lesson(
            curriculum_id=curriculum_id,
            week_number=week_number,
            lesson=lesson,
            lesson_index=insert_index,
        )

        week_schedule.lessons = Lessons(
            week_schedule.lessons.items[:insert_index]
            + [lesson]
            + week_schedule.lessons.items[insert_index:]
        )
        return curriculum

        # updated = await self.curriculum_repo.find_by_id(
        #     id=curriculum_id,
        #     owner_id=owner_id,
        #     role=role,
        # )
        # if not updated:
        #     raise CurriculumNotFoundError(f"{curriculum_id} not found after insert")
        # return updated

    async def update_lesson(
        self,
        curriculum_id: str,
        owner_id: str,
        role: RoleVO,
        week_number: int,
        lesson_index: int,
        new_lesson: str,
    ) -> Curriculum:

        curriculum = await self.curriculum_repo.find_by_id(
            id=curriculum_id,
            owner_id=owner_id,
            role=role,
        )

        if not curriculum:
            raise CurriculumNotFoundError(f"{curriculum_id} curriculum not found")

        week_schedule = next(
            (
                week
                for week in curriculum.week_schedules
                if week.week_number.value == week_number
            ),
            None,
        )

        if not week_schedule:
            raise WeekScheduleNotFoundError(f"Week {week_number} not found")

        if not (0 <= lesson_index < len(week_schedule.lessons.items)):
            raise WeekIndexOutOfRangeError("lesson_index out of range")

        lessons_list = week_schedule.lessons.items
        lessons_list[lesson_index] = new_lesson

        await self.curriculum_repo.update_week_schedule(
            curriculum_id=curriculum_id,
            week_number=week_number,
            lessons=lessons_list,
        )

        week_schedule.lessons = Lessons(lessons_list)

        return curriculum

    async def delete_lesson(
        self,
        curriculum_id: str,
        owner_id: str,
        role: RoleVO,
        week_number: int,
        lesson_index: int,
    ) -> Curriculum:

        curriculum = await self.curriculum_repo.find_by_id(
            id=curriculum_id,
            role=role,
            owner_id=owner_id,
        )

        if not curriculum:
            raise CurriculumNotFoundError(f"Curriculum {curriculum_id} not found")

        if role != RoleVO.ADMIN and curriculum.owner_id != owner_id:
            raise PermissionError("권한이 없습니다")

        week_schedule = next(
            (
                week_schedule
                for week_schedule in curriculum.week_schedules
                if week_schedule.week_number.value == week_number
            ),
            None,
        )
        if not week_schedule:
            raise WeekScheduleNotFoundError(f"Week {week_number} not found")

        if not (0 <= lesson_index < week_schedule.lessons.count):
            raise WeekIndexOutOfRangeError("lesson_index out of range")

        await self.curriculum_repo.delete_lesson(
            curriculum_id=curriculum_id,
            week_number=week_number,
            lesson_index=lesson_index,
        )

        lessons = week_schedule.lessons.items
        lessons.pop(lesson_index)
        week_schedule.lessons = Lessons(lessons)

        return curriculum
