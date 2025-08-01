from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field
from curriculum.domain.entity.curriculum import Curriculum
from curriculum.interface.schemas.curriculum_schema import WeekScheduleItem
from user.domain.entity.user import User
from user.domain.value_object.role import RoleVO
from user.interface.schemas.user_schema import UpdateUserBody


class AdminGetUserResponse(BaseModel):
    """Admin 전용 User 조회 응답 - 모든 정보 포함"""

    id: str
    name: str = Field(min_length=2, max_length=32)
    email: EmailStr = Field(max_length=64)
    role: str
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_domain(cls, user: User) -> "AdminGetUserResponse":
        return cls(
            id=user.id,
            name=str(user.name),
            email=str(user.email),
            role=user.role.value,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )


class AdminGetUsersPageResponse(BaseModel):
    """Admin 전용 User 목록 응답"""

    total_count: int
    page: int
    items_per_page: int
    users: List[AdminGetUserResponse]

    @classmethod
    def from_domain(
        cls,
        total_count: int,
        page: int,
        items_per_page: int,
        users: List[AdminGetUserResponse],
    ) -> "AdminGetUsersPageResponse":  # 올바른 리턴 타입
        return cls(
            total_count=total_count,
            page=page,
            items_per_page=items_per_page,
            users=users,
        )


class AdminUpdateUserBody(UpdateUserBody):
    """Admin 전용 User 수정 요청 - role 포함"""

    role: Optional[RoleVO] = None


class AdminUpdateUserResponse(BaseModel):
    """Admin 전용 User 수정 응답 - 모든 정보 포함"""

    id: str
    name: str = Field(min_length=2, max_length=32)
    email: EmailStr = Field(max_length=64)
    role: str
    updated_at: datetime

    @classmethod
    def from_domain(cls, user: User) -> "AdminUpdateUserResponse":
        return cls(
            id=user.id,
            name=str(user.name),
            email=str(user.email),
            role=user.role.value,
            updated_at=user.updated_at,
        )


class AdminGetCurriculumResponse(BaseModel):
    """Admin 전용 Curriculum 조회 응답 - 모든 정보 포함"""

    id: str
    owner_id: str
    owner_name: str
    title: str
    visibility: str
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
            owner_name=getattr(curriculum, "owner_name", "Unknown"),  # admin
            title=str(curriculum.title),
            visibility=curriculum.visibility.value,
            week_schedules=week_schedule_items,
            created_at=curriculum.created_at,
            updated_at=curriculum.updated_at,
        )


class AdminGetCurriculumsPageResponse(BaseModel):

    total_count: int
    page: int
    items_per_page: int
    curriculums: List[AdminGetCurriculumResponse]

    @classmethod
    def from_domain(
        cls,
        total_count: int,
        page: int,
        items_per_page: int,
        curriculums: List[AdminGetCurriculumResponse],
    ) -> "AdminGetCurriculumsPageResponse":
        return cls(
            total_count=total_count,
            page=page,
            items_per_page=items_per_page,
            curriculums=curriculums,
        )
