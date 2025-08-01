from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from dependency_injector.wiring import inject, Provide

from common.auth import CurrentUser, get_current_user, Role

from admin.interface.schemas.admin_summary_schema import (
    AdminGetSummaryResponse,
    AdminGetSummariesPageResponse,
)

from DI.containers import Container
from curriculum.application.summary_service import SummaryService


router = APIRouter(prefix="/admins/summaries", tags=["admin/summaries"])


def assert_admin(current_user: CurrentUser) -> None:
    if current_user.role != Role.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="관리자만 접근이 가능합니다."
        )


@router.get("/", status_code=200, response_model=AdminGetSummariesPageResponse)
@inject
async def get_summaries_for_admin(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    page: int = 1,
    items_per_page: int = 10,
    summary_service: SummaryService = Depends(Provide[Container.summary_service]),
):
    """관리자가 모든 요약 조회"""
    assert_admin(current_user)

    # 모든 사용자의 요약을 조회하기 위해 새로운 서비스 메서드 필요
    # 임시로 빈 owner_id로 처리 (추후 SummaryService에 admin용 메서드 추가 필요)
    total_count, summaries = await summary_service.get_all_summaries_for_admin(
        # owner_id="",  # Admin용으로 수정 필요
        page=page,
        items_per_page=items_per_page,
    )

    summary_responses: list[AdminGetSummaryResponse] = [
        AdminGetSummaryResponse.from_domain(s) for s in summaries
    ]

    return AdminGetSummariesPageResponse.from_domain(
        total_count=total_count,
        page=page,
        items_per_page=items_per_page,
        summaries=summary_responses,
    )


@router.get("/{summary_id}", status_code=200, response_model=AdminGetSummaryResponse)
@inject
async def get_summary_by_id_for_admin(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    summary_id: str,
    summary_service: SummaryService = Depends(Provide[Container.summary_service]),
):
    """관리자가 특정 요약 상세 조회"""
    assert_admin(current_user)

    summary, feedback = await summary_service.get_summary(
        owner_id="",  # Admin은 모든 요약 접근 가능 (서비스 레벨에서 처리)
        summary_id=summary_id,
        role=current_user.role,
    )
    return AdminGetSummaryResponse.from_domain(summary, feedback)


@router.delete("/{summary_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_summary_by_admin(
    summary_id: str,
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    summary_service: SummaryService = Depends(Provide[Container.summary_service]),
):
    """관리자가 요약 삭제"""
    assert_admin(current_user)

    await summary_service.delete_summary(
        owner_id="",  # Admin은 소유자 체크 안함
        role=current_user.role,
        summary_id=summary_id,
    )
