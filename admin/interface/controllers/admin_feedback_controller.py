from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from dependency_injector.wiring import inject, Provide

from common.auth import CurrentUser, get_current_user, Role

from admin.interface.schemas.admin_feedback_schema import (
    AdminGetFeedbackResponse,
    AdminGetFeedbacksPageResponse,
)

from DI.containers import Container
from curriculum.application.feedback_service import FeedbackService


router = APIRouter(prefix="/admins/feedbacks", tags=["admin/feedbacks"])


def assert_admin(current_user: CurrentUser) -> None:
    if current_user.role != Role.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="관리자만 접근이 가능합니다."
        )


@router.get("/", status_code=200, response_model=AdminGetFeedbacksPageResponse)
@inject
async def get_feedbacks_for_admin(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    page: int = 1,
    items_per_page: int = 10,
    feedback_service: FeedbackService = Depends(Provide[Container.feedback_service]),
):
    """관리자가 모든 피드백 조회 (구현 필요: FeedbackService에 admin용 메서드 추가)"""
    assert_admin(current_user)

    total_count, feedbacks = await feedback_service.get_all_feedbacks_for_admin(
        page=page,
        items_per_page=items_per_page,
    )

    feedback_responses: list[AdminGetFeedbackResponse] = [
        AdminGetFeedbackResponse.from_domain(fb) for fb in feedbacks
    ]
    return AdminGetFeedbacksPageResponse.from_domain(
        total_count=total_count,
        page=page,
        items_per_page=items_per_page,
        feedbacks=feedback_responses,
    )


@router.delete("/{feedback_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_feedback_by_admin(
    feedback_id: str,
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    feedback_service: FeedbackService = Depends(Provide[Container.feedback_service]),
):
    """관리자가 피드백 삭제"""
    assert_admin(current_user)

    await feedback_service.delete_feedback(
        owner_id="",  # Admin은 소유자 체크 안함
        role=current_user.role,
        curriculum_id="",  # 필요시 조회해서 채우기
        summary_id="",  # 필요시 조회해서 채우기
        feedback_id=feedback_id,
    )
