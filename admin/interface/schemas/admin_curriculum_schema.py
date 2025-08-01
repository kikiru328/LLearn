from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

from curriculum.domain.entity.curriculum import Curriculum

# from curriculum.domain.value_object.visibility import Visibility
from curriculum.interface.schemas.curriculum_schema import (
    WeekScheduleItem,
    VisibilityEnum,
)


class AdminGetCurriculumResponse(BaseModel):
    """Admin 전용 Curriculum 조회 응답 - 모든 정보 포함"""

    id: str
    owner_id: str
    owner_name: str
    title: str = Field(min_length=2, max_length=50)
    visibility: VisibilityEnum
    week_schedules: List[WeekScheduleItem]
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_domain(cls, curriculum: Curriculum) -> "AdminGetCurriculumResponse":
        week_schedule_items = [
            WeekScheduleItem(
                week_number=week_schedule.week_number.value,
                lessons=week_schedule.lessons.items,
            )
            for week_schedule in curriculum.week_schedules
        ]

        return cls(
            id=curriculum.id,
            owner_id=curriculum.owner_id,
            owner_name=getattr(curriculum, "owner_name", "Unknown"),
            title=str(curriculum.title),
            visibility=VisibilityEnum(curriculum.visibility.value),
            week_schedules=week_schedule_items,
            created_at=curriculum.created_at,
            updated_at=curriculum.updated_at,
        )


class AdminGetCurriculumsPageResponse(BaseModel):
    """Admin 전용 Curriculum 목록 응답"""

    total_count: int
    page: int
    items_per_page: int
    curricula: List[AdminGetCurriculumResponse]

    @classmethod
    def from_domain(
        cls,
        total_count: int,
        page: int,
        items_per_page: int,
        curricula: List[AdminGetCurriculumResponse],
    ) -> "AdminGetCurriculumsPageResponse":
        return cls(
            total_count=total_count,
            page=page,
            items_per_page=items_per_page,
            curricula=curricula,
        )


class AdminUpdateCurriculumBody(BaseModel):
    """Admin 전용 Curriculum 수정 요청"""

    title: Optional[str] = Field(None, min_length=2, max_length=50)
    visibility: Optional[VisibilityEnum] = None


class AdminUpdateCurriculumResponse(BaseModel):
    """Admin 전용 Curriculum 수정 응답"""

    id: str
    owner_id: str
    owner_name: str
    title: str = Field(min_length=2, max_length=50)
    visibility: VisibilityEnum
    updated_at: datetime

    @classmethod
    def from_domain(cls, curriculum: Curriculum) -> "AdminUpdateCurriculumResponse":
        return cls(
            id=curriculum.id,
            owner_id=curriculum.owner_id,
            owner_name=getattr(curriculum, "owner_name", "Unknown"),
            title=str(curriculum.title),
            visibility=VisibilityEnum(curriculum.visibility.value),
            updated_at=curriculum.updated_at,
        )
