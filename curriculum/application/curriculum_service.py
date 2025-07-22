from datetime import datetime, timezone
from typing import List
from ulid import ULID
from curriculum.application.exception import CurriculumNotFoundError
from curriculum.domain.entity.curriculum import Curriculum
from curriculum.domain.entity.week_schedule import WeekSchedule
from curriculum.domain.repository.curriculum_repo import ICurriculumRepository
from curriculum.domain.value_object.title import Title


class CurriculumService:
    def __init__(
        self,
        curriculum_repo: ICurriculumRepository,
    ) -> None:
        self.curriculum_repo: ICurriculumRepository = curriculum_repo

    async def create_curriculum(
        self,
        title: str,
        week_schedules: List[WeekSchedule],
        created_at: datetime | None = None,
    ) -> Curriculum:
        created_at = created_at or datetime.now(timezone.utc)
        id = ULID()  # new_id
        curriculum = Curriculum(
            id=id,
            title=Title(title),
            created_at=created_at,
            updated_at=created_at,
            week_schedules=week_schedules,
        )

        await self.curriculum_repo.save(curriculum)
        return curriculum

    async def get_curriculum_by_id(
        self,
        curriculum_id: ULID,
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
        curriculum_id: ULID,
        title: str,
    ):
        curriculum = await self.get_curriculum_by_id(curriculum_id)
        curriculum.title = Title(title)
        curriculum.updated_at = datetime.now(timezone.utc)

        await self.curriculum_repo.update(curriculum)
        return curriculum

    async def delete_curriculum(
        self,
        curriculum_id: ULID,
    ):
        existing = await self.curriculum_repo.find_by_id(curriculum_id)
        if existing is None:
            raise CurriculumNotFoundError(f"curriculum {curriculum_id} not found")

        await self.curriculum_repo.delete(curriculum_id)
