from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from dependency_injector.wiring import inject, Provide

from common.auth import CurrentUser, get_current_user, Role

from admin.interface.schemas.admin_stats_schema import (
    AdminStatsResponse,
    AdminDashboardResponse,
)

from DI.containers import Container
from user.application.user_service import UserService
from curriculum.application.curriculum_service import CurriculumService
from curriculum.application.summary_service import SummaryService
from curriculum.application.feedback_service import FeedbackService


router = APIRouter(prefix="/admins", tags=["admin-stats"])


def assert_admin(current_user: CurrentUser) -> None:
    if current_user.role != Role.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="관리자만 접근이 가능합니다."
        )


@router.get("/stats", status_code=200, response_model=AdminStatsResponse)
@inject
async def get_admin_stats(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    user_service: UserService = Depends(Provide[Container.user_service]),
    curriculum_service: CurriculumService = Depends(
        Provide[Container.curriculum_service]
    ),
    summary_service: SummaryService = Depends(Provide[Container.summary_service]),
    feedback_service: FeedbackService = Depends(Provide[Container.feedback_service]),
):
    """관리자 통계 조회"""
    assert_admin(current_user)

    # 사용자 수
    total_users, _ = await user_service.get_users(page=1, items_per_page=1)

    # 커리큘럼 수 (Admin 권한으로 모든 커리큘럼 조회)
    total_curriculums, _ = await curriculum_service.get_curriculums(
        owner_id=None,
        role=current_user.role,
        page=1,
        items_per_page=1,
    )

    # 요약 수
    total_summaries = await summary_service.get_total_summaries_count()

    # 피드백 수
    total_feedbacks = await feedback_service.get_total_feedbacks_count()

    return AdminStatsResponse(
        total_users=total_users,
        total_curriculums=total_curriculums,
        total_summaries=total_summaries,
        total_feedbacks=total_feedbacks,
    )


@router.get("/dashboard", status_code=200, response_model=AdminDashboardResponse)
@inject
async def get_admin_dashboard(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    user_service: UserService = Depends(Provide[Container.user_service]),
    curriculum_service: CurriculumService = Depends(
        Provide[Container.curriculum_service]
    ),
):
    """관리자 대시보드 데이터 조회"""
    assert_admin(current_user)

    # 최근 사용자 목록
    _, recent_users = await user_service.get_users(page=1, items_per_page=5)

    # 최근 커리큘럼 목록
    _, recent_curriculums = await curriculum_service.get_curriculums(
        owner_id=None,
        role=current_user.role,
        page=1,
        items_per_page=5,
    )

    return AdminDashboardResponse.from_domain(
        recent_users=recent_users,
        recent_curriculums=recent_curriculums,
    )
