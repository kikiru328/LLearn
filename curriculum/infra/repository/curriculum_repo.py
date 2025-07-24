from typing import List, Tuple
from ulid import ULID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from curriculum.infra.db_models.curriculum import CurriculumModel, WeekScheduleModel
from curriculum.domain.entity.curriculum import Curriculum
from curriculum.domain.entity.week_schedule import WeekSchedule
from curriculum.domain.value_object.title import Title
from curriculum.domain.value_object.week_number import WeekNumber
from curriculum.domain.value_object.topics import Topics
from typing import cast
from datetime import datetime


class CurriculumRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, curriculum: Curriculum) -> None:
        curriculum_model = CurriculumModel(
            id=str(curriculum.id),
            user_id=str(curriculum.owner_id),
            title=str(curriculum.title),
            created_at=curriculum.created_at,
            updated_at=curriculum.updated_at,
        )
        for week_schedule in curriculum.week_schedules:
            schedule_model = WeekScheduleModel(
                week_number=week_schedule.week_number.value,
                topics=week_schedule.topics.items,
            )
            curriculum_model.week_schedules.append(schedule_model)
        self.session.add(curriculum_model)
        await self.session.commit()

    async def find_by_id(self, curriculum_id: ULID) -> Curriculum | None:
        query_result = await self.session.execute(
            select(CurriculumModel).where(CurriculumModel.id == str(curriculum_id))
        )
        curriculum_model = query_result.scalar_one_or_none()
        if curriculum_model is None:
            return None

        week_schedules: List[WeekSchedule] = []
        for schedule_model in curriculum_model.week_schedules:
            week_schedules.append(
                WeekSchedule(
                    week_number=WeekNumber(schedule_model.week_number),
                    topics=Topics(schedule_model.topics),
                )
            )

        created_at = cast(datetime, curriculum_model.created_at)
        updated_at = cast(datetime, curriculum_model.updated_at)

        return Curriculum(
            id=ULID(curriculum_model.id),
            owner_id=ULID(curriculum_model.user_id),
            title=Title(curriculum_model.title),
            created_at=created_at,
            updated_at=updated_at,
            week_schedules=week_schedules,
        )

    async def find_curriculums(
        self, page: int, items_per_page: int
    ) -> Tuple[int, List[Curriculum]]:
        query_result = await self.session.execute(select(CurriculumModel))
        all_models = query_result.scalars().all()
        total_count = len(all_models)
        paginated_models = all_models[
            (page - 1) * items_per_page : page * items_per_page
        ]

        curriculums: List[Curriculum] = []
        for curriculum_model in paginated_models:
            week_schedules: List[WeekSchedule] = []
            for schedule_model in curriculum_model.week_schedules:
                week_schedules.append(
                    WeekSchedule(
                        week_number=WeekNumber(schedule_model.week_number),
                        topics=Topics(schedule_model.topics),
                    )
                )
            created_at = cast(datetime, curriculum_model.created_at)
            updated_at = cast(datetime, curriculum_model.updated_at)

            curriculums.append(
                Curriculum(
                    id=ULID(curriculum_model.id),
                    owner_id=ULID(curriculum_model.user_id),
                    title=Title(curriculum_model.title),
                    created_at=created_at,
                    updated_at=updated_at,
                    week_schedules=week_schedules,
                )
            )
        return total_count, curriculums

    async def update(self, curriculum: Curriculum) -> None:
        await self.session.execute(
            update(CurriculumModel)
            .where(CurriculumModel.id == str(curriculum.id))
            .values(
                title=str(curriculum.title),
                updated_at=curriculum.updated_at,
            )
        )
        await self.session.commit()

    async def delete(self, curriculum_id: ULID) -> None:
        await self.session.execute(
            delete(CurriculumModel).where(CurriculumModel.id == str(curriculum_id))
        )
        await self.session.commit()
