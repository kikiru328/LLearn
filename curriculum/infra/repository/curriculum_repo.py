from typing import Any, List, Optional, Tuple
from sqlalchemy import func, or_, select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.selectable import Select
from sqlalchemy.orm import selectinload, joinedload
from curriculum.application.exception import (
    CurriculumNotFoundError,
    WeekIndexOutOfRangeError,
    WeekScheduleNotFoundError,
)
from curriculum.domain.entity.curriculum import Curriculum
from curriculum.domain.entity.week_schedule import WeekSchedule
from curriculum.domain.repository.curriculum_repo import ICurriculumRepository
from curriculum.domain.value_object.lessons import Lessons
from curriculum.domain.value_object.title import Title
from curriculum.domain.value_object.visibility import Visibility
from curriculum.domain.value_object.week_number import WeekNumber
from curriculum.infra.db_models.curriculum import CurriculumModel
from curriculum.infra.db_models.week_schedule import WeekScheduleModel
from user.domain.value_object.role import RoleVO


class CurriculumRepository(ICurriculumRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session: AsyncSession = session

    def _map_to_entity(self, curriculum_model: CurriculumModel) -> Curriculum:
        week_schedules_model = sorted(
            curriculum_model.week_schedules,
            key=lambda week_schedule: week_schedule.week_number,
        )
        return Curriculum(
            id=curriculum_model.id,
            owner_id=curriculum_model.user_id,
            title=Title(curriculum_model.title),
            visibility=Visibility(curriculum_model.visibility),
            created_at=curriculum_model.created_at,
            updated_at=curriculum_model.updated_at,
            week_schedules=[
                WeekSchedule(
                    week_number=WeekNumber(week_schedule.week_number),
                    lessons=Lessons(week_schedule.lessons),
                )
                for week_schedule in week_schedules_model
            ],
        )

    async def create(self, curriculum: Curriculum) -> None:
        new_curriculum = CurriculumModel(
            id=str(curriculum.id),
            user_id=str(curriculum.owner_id),
            title=str(curriculum.title),
            visibility=curriculum.visibility.value,
            created_at=curriculum.created_at,
            updated_at=curriculum.updated_at,
        )

        for week_schedule in curriculum.week_schedules:
            new_curriculum.week_schedules.append(
                WeekScheduleModel(
                    week_number=week_schedule.week_number.value,
                    lessons=week_schedule.lessons.items,
                )
            )

        self.session.add(new_curriculum)
        await self.session.commit()

    async def update(self, curriculum: Curriculum) -> None:
        existing_curriculum: CurriculumModel | None = await self.session.get(
            CurriculumModel, str(curriculum.id)
        )

        if existing_curriculum is None:
            raise CurriculumNotFoundError(f"{curriculum.id} not found")

        existing_curriculum.title = str(curriculum.title)
        existing_curriculum.visibility = curriculum.visibility.value
        existing_curriculum.updated_at = curriculum.updated_at  # datetime 할당
        self.session.add(existing_curriculum)
        try:
            await self.session.commit()
        except:
            await self.session.rollback()
            raise

    async def delete(self, id: str) -> None:
        existing_curriculum: CurriculumModel | None = await self.session.get(
            CurriculumModel, id
        )

        if not existing_curriculum:
            raise CurriculumNotFoundError(f"curriculum with id={id} not found")

        await self.session.delete(existing_curriculum)
        try:
            await self.session.commit()
        except:
            await self.session.rollback()
            raise

    async def count_owner(self, owner_id: str) -> int:
        query = (
            select(func.count())
            .select_from(CurriculumModel)
            .where(CurriculumModel.user_id == owner_id)
        )
        return await self.session.scalar(query)

    async def find_by_id(
        self,
        id: str,
        owner_id: Optional[str] = None,
        role: RoleVO = RoleVO.USER,
    ) -> Optional[Curriculum]:
        query = (
            select(CurriculumModel)
            .where(CurriculumModel.id == id)
            .options(
                selectinload(CurriculumModel.week_schedules),
                joinedload(CurriculumModel.user),  # user 로드
            )
        )
        if role != RoleVO.ADMIN:
            query = query.where(
                or_(
                    CurriculumModel.user_id == owner_id,
                    CurriculumModel.visibility == Visibility.PUBLIC.value,
                )
            )
        query = query.options(selectinload(CurriculumModel.week_schedules))
        result = await self.session.execute(query)
        curriculum: Any | None = result.scalars().first()
        if not curriculum:
            return None
        curriculum_entity = self._map_to_entity(curriculum)
        setattr(curriculum_entity, "owner_name", curriculum.user.name)  # add
        return curriculum_entity

    async def find_by_title(
        self,
        title: Title,
        owner_id: Optional[str] = None,
        role: RoleVO = RoleVO.USER,
    ) -> Optional[Curriculum]:
        query: Select = select(CurriculumModel).where(
            CurriculumModel.title == str(title)
        )
        if role != RoleVO.ADMIN:
            query = query.where(
                or_(
                    CurriculumModel.user_id == owner_id,  # 자신이거나
                    CurriculumModel.visibility
                    == Visibility.PUBLIC.value,  # Public이거나
                )
            )
        query = query.options(selectinload(CurriculumModel.week_schedules))
        result = await self.session.execute(query)
        curriculum = result.scalars().first()
        if not curriculum:
            return None
        return Curriculum(
            id=curriculum.id,
            owner_id=curriculum.user_id,
            title=Title(curriculum.title),
            visibility=Visibility(curriculum.visibility),
            created_at=curriculum.created_at,
            updated_at=curriculum.updated_at,
            week_schedules=[
                WeekSchedule(
                    week_number=WeekNumber(week_schedule.week_number),
                    lessons=Lessons(week_schedule.lessons),
                )
                for week_schedule in curriculum.week_schedules
            ],
        )

    async def find_curriculums(
        self,
        page: int = 1,
        items_per_page: int = 10,
        owner_id: Optional[str] = None,
        role: RoleVO = RoleVO.USER,
    ) -> Tuple[int, List[Curriculum]]:
        query = select(CurriculumModel).options(
            selectinload(CurriculumModel.week_schedules),
            joinedload(CurriculumModel.user),  # <-- user 관계 로드
        )
        if role != RoleVO.ADMIN:
            query = query.where(CurriculumModel.user_id == owner_id)

        # total count in subquery
        count_query = select(func.count()).select_from(query.subquery())
        total_count = await self.session.scalar(count_query)

        # paging
        offset = (page - 1) * items_per_page

        paged_query = (
            query.order_by(CurriculumModel.created_at.desc())
            .limit(items_per_page)
            .offset(offset)
            .options(selectinload(CurriculumModel.week_schedules))
        )
        result = await self.session.execute(paged_query)
        curriculums_models = result.scalars().all()

        curriculums = []
        for curriculum_model in curriculums_models:
            curriculum = Curriculum(
                id=curriculum_model.id,
                owner_id=curriculum_model.user_id,
                title=Title(curriculum_model.title),
                visibility=Visibility(curriculum_model.visibility),
                created_at=curriculum_model.created_at,
                updated_at=curriculum_model.updated_at,
                week_schedules=[
                    WeekSchedule(
                        week_number=WeekNumber(ws.week_number),
                        lessons=Lessons(ws.lessons),
                    )
                    for ws in curriculum_model.week_schedules
                ],
            )
            setattr(
                curriculum, "owner_name", curriculum_model.user.name
            )  # <-- owner_name 주입
            curriculums.append(curriculum)

        return total_count, curriculums

    async def insert_week_and_shift(
        self,
        curriculum_id: str,
        new_week_number: int,
        lessons: Lessons,
    ):

        await self.session.execute(
            update(WeekScheduleModel)
            .where(
                WeekScheduleModel.curriculum_id == curriculum_id,
                WeekScheduleModel.week_number >= new_week_number,
            )
            .values(week_number=WeekScheduleModel.week_number + 1)
        )

        # insert
        new_model = WeekScheduleModel(
            curriculum_id=curriculum_id,
            week_number=new_week_number,
            lessons=lessons,
        )
        self.session.add(new_model)

        try:
            await self.session.commit()
        except:
            await self.session.rollback()
            raise

    async def delete_week_and_shift(
        self,
        curriculum_id: str,
        week_number: int,
    ):

        await self.session.execute(
            delete(WeekScheduleModel).where(
                WeekScheduleModel.curriculum_id == curriculum_id,
                WeekScheduleModel.week_number == week_number,
            )
        )

        await self.session.execute(
            update(WeekScheduleModel)
            .where(
                WeekScheduleModel.curriculum_id == curriculum_id,
                WeekScheduleModel.week_number > week_number,
            )
            .values(week_number=WeekScheduleModel.week_number - 1)
        )
        await self.session.commit()

    async def insert_lesson(
        self,
        curriculum_id: str,
        week_number: int,
        lesson: str,
        lesson_index: int,
    ):
        query = select(WeekScheduleModel).where(
            WeekScheduleModel.curriculum_id == curriculum_id,
            WeekScheduleModel.week_number == week_number,
        )
        result = await self.session.execute(query)
        week_schedule_model = result.scalars().first()
        if not week_schedule_model:
            raise WeekScheduleNotFoundError(f"week {week_number} not found")

        lessons: List[str] = week_schedule_model.lessons or []
        lessons.insert(lesson_index, lesson)
        week_schedule_model.lessons = lessons

        await self.session.execute(
            update(WeekScheduleModel)
            .where(
                WeekScheduleModel.curriculum_id == curriculum_id,
                WeekScheduleModel.week_number == week_number,
            )
            .values(lessons=lessons)
        )

        try:
            self.session.add(week_schedule_model)
            await self.session.commit()
        except:
            await self.session.rollback()
            raise

    async def update_week_schedule(
        self,
        curriculum_id: str,
        week_number: int,
        lessons: List[str],
    ):
        query = select(WeekScheduleModel).where(
            WeekScheduleModel.curriculum_id == curriculum_id,
            WeekScheduleModel.week_number == week_number,
        )
        result = await self.session.execute(query)
        week_schedule_model = result.scalars().first()
        if not week_schedule_model:
            raise WeekScheduleNotFoundError(
                f"Week {week_number} not found in curriculum {curriculum_id}"
            )

        week_schedule_model.lessons = lessons
        try:
            self.session.add(week_schedule_model)
            await self.session.commit()
        except:
            await self.session.rollback()
            raise

    async def delete_lesson(
        self,
        curriculum_id: str,
        week_number: int,
        lesson_index: int,
    ):
        query = select(WeekScheduleModel).where(
            WeekScheduleModel.curriculum_id == curriculum_id,
            WeekScheduleModel.week_number == week_number,
        )
        result = await self.session.execute(query)
        week_schedule_model = result.scalars().first()
        if not week_schedule_model:
            raise WeekScheduleNotFoundError(f"Week {week_number} not found")

        lessons: List[str] = week_schedule_model.lessons or []

        if not (0 <= lesson_index < len(lessons)):
            raise WeekIndexOutOfRangeError("lesson_index out of range")

        lessons.pop(lesson_index)
        week_schedule_model.lessons = lessons

        await self.session.execute(
            update(WeekScheduleModel)
            .where(
                WeekScheduleModel.curriculum_id == curriculum_id,
                WeekScheduleModel.week_number == week_number,
            )
            .values(lessons=lessons)
        )

        try:
            self.session.add(week_schedule_model)
            await self.session.commit()

        except:
            await self.session.rollback()
            raise
