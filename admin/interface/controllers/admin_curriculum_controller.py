from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from dependency_injector.wiring import inject, Provide

from common.auth import CurrentUser, get_current_user, Role

from admin.interface.schemas.admin_curriculum_schema import (
    AdminGetCurriculumResponse,
    AdminGetCurriculumsPageResponse,
    AdminUpdateCurriculumResponse,
    AdminUpdateCurriculumBody,
)

from DI.containers import Container
from curriculum.application.curriculum_service import CurriculumService


router = APIRouter(prefix="/admins/curriculums", tags=["admin/curriculums"])


def assert_admin(current_user: CurrentUser) -> None:
    if current_user.role != Role.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="관리자만 접근이 가능합니다."
        )


@router.get("/", status_code=200, response_model=AdminGetCurriculumsPageResponse)
@inject
async def get_curriculums_for_admin(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    page: int = 1,
    items_per_page: int = 10,
    curriculum_service: CurriculumService = Depends(
        Provide[Container.curriculum_service]
    ),
):
    """관리자가 모든 커리큘럼 조회"""
    assert_admin(current_user)

    total_count, curriculums = await curriculum_service.get_curriculums(
        owner_id=None,  # Admin은 모든 커리큘럼 조회
        role=current_user.role,
        page=page,
        items_per_page=items_per_page,
    )

    curricula: list[AdminGetCurriculumResponse] = [
        AdminGetCurriculumResponse.from_domain(c) for c in curriculums
    ]

    return AdminGetCurriculumsPageResponse.from_domain(
        total_count=total_count,
        page=page,
        items_per_page=items_per_page,
        curricula=curricula,
    )


@router.get(
    "/{curriculum_id}", status_code=200, response_model=AdminGetCurriculumResponse
)
@inject
async def get_curriculum_by_id_for_admin(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    curriculum_id: str,
    curriculum_service: CurriculumService = Depends(
        Provide[Container.curriculum_service]
    ),
):
    """관리자가 특정 커리큘럼 상세 조회"""
    assert_admin(current_user)

    curriculum = await curriculum_service.get_curriculum_by_id(
        curriculum_id=curriculum_id,
        owner_id=None,  # Admin은 모든 커리큘럼 접근 가능
        role=current_user.role,
    )
    return AdminGetCurriculumResponse.from_domain(curriculum)


@router.patch(
    "/{curriculum_id}", status_code=200, response_model=AdminUpdateCurriculumResponse
)
@inject
async def update_curriculum_by_admin(
    curriculum_id: str,
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    body: AdminUpdateCurriculumBody,
    curriculum_service: CurriculumService = Depends(
        Provide[Container.curriculum_service]
    ),
) -> AdminUpdateCurriculumResponse:
    """관리자가 커리큘럼 수정"""
    assert_admin(current_user)

    updated_curriculum = await curriculum_service.update_curriculum(
        curriculum_id=curriculum_id,
        owner_id=None,  # Admin은 소유자 체크 안함
        role=current_user.role,
        title=body.title,
        visibility=body.visibility,
    )
    return AdminUpdateCurriculumResponse.from_domain(updated_curriculum)


@router.delete("/{curriculum_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_curriculum_by_admin(
    curriculum_id: str,
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    curriculum_service: CurriculumService = Depends(
        Provide[Container.curriculum_service]
    ),
):
    """관리자가 커리큘럼 삭제"""
    assert_admin(current_user)

    await curriculum_service.delete_curriculum(
        id=curriculum_id,
        owner_id=None,  # Admin은 소유자 체크 안함
        role=current_user.role,
    )
