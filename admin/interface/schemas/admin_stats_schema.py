from datetime import datetime
from typing import List
from pydantic import BaseModel

from user.domain.entity.user import User
from curriculum.domain.entity.curriculum import Curriculum


class AdminStatsResponse(BaseModel):
    """관리자 통계 응답"""

    total_users: int
    total_curriculums: int
    total_summaries: int
    total_feedbacks: int


class AdminRecentUserResponse(BaseModel):
    """최근 사용자 정보"""

    id: str
    name: str
    email: str
    role: str
    created_at: datetime

    @classmethod
    def from_domain(cls, user: User) -> "AdminRecentUserResponse":
        return cls(
            id=user.id,
            name=str(user.name),
            email=str(user.email),
            role=user.role.value,
            created_at=user.created_at,
        )


class AdminRecentCurriculumResponse(BaseModel):
    """최근 커리큘럼 정보"""

    id: str
    title: str
    owner_name: str
    visibility: str
    created_at: datetime

    @classmethod
    def from_domain(cls, curriculum: Curriculum) -> "AdminRecentCurriculumResponse":
        return cls(
            id=curriculum.id,
            title=str(curriculum.title),
            owner_name=getattr(curriculum, "owner_name", "Unknown"),
            visibility=curriculum.visibility.value,
            created_at=curriculum.created_at,
        )


class AdminDashboardResponse(BaseModel):
    """관리자 대시보드 응답"""

    recent_users: List[AdminRecentUserResponse]
    recent_curriculums: List[AdminRecentCurriculumResponse]

    @classmethod
    def from_domain(
        cls,
        recent_users: List[User],
        recent_curriculums: List[Curriculum],
    ) -> "AdminDashboardResponse":
        return cls(
            recent_users=[
                AdminRecentUserResponse.from_domain(user) for user in recent_users
            ],
            recent_curriculums=[
                AdminRecentCurriculumResponse.from_domain(curriculum)
                for curriculum in recent_curriculums
            ],
        )
