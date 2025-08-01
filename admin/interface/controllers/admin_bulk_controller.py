from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from dependency_injector.wiring import inject, Provide

from common.auth import CurrentUser, get_current_user, Role

from admin.interface.schemas.admin_bulk_schema import (
    BulkDeleteCurriculumsRequest,
    BulkDeleteCurriculumsResponse,
    BulkUpdateCurriculumsRequest,
    BulkUpdateCurriculumsResponse,
    BulkDeleteUsersRequest,
    BulkDeleteUsersResponse,
)

from DI.containers import Container
from curriculum.application.curriculum_service import CurriculumService
from user.application.user_service import UserService


router = APIRouter(prefix="/admins", tags=["admin/bulk-operations"])


def assert_admin(current_user: CurrentUser) -> None:
    if current_user.role != Role.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="관리자만 접근이 가능합니다."
        )


@router.delete(
    "/bulk/curriculums", status_code=200, response_model=BulkDeleteCurriculumsResponse
)
@inject
async def bulk_delete_curriculums(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    request: BulkDeleteCurriculumsRequest,
    curriculum_service: CurriculumService = Depends(
        Provide[Container.curriculum_service]
    ),
):
    """여러 커리큘럼 일괄 삭제"""
    assert_admin(current_user)

    deleted_ids = []
    failed_ids = []

    for curriculum_id in request.curriculum_ids:
        try:
            await curriculum_service.delete_curriculum(
                id=curriculum_id,
                owner_id=None,  # Admin은 소유자 체크 안함
                role=current_user.role,
            )
            deleted_ids.append(curriculum_id)
        except Exception as e:
            failed_ids.append({"id": curriculum_id, "error": str(e)})

    return BulkDeleteCurriculumsResponse(
        deleted_count=len(deleted_ids),
        deleted_ids=deleted_ids,
        failed_count=len(failed_ids),
        failed_items=failed_ids,
    )


@router.patch(
    "/bulk/curriculums", status_code=200, response_model=BulkUpdateCurriculumsResponse
)
@inject
async def bulk_update_curriculums(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    request: BulkUpdateCurriculumsRequest,
    curriculum_service: CurriculumService = Depends(
        Provide[Container.curriculum_service]
    ),
):
    """여러 커리큘럼 일괄 수정"""
    assert_admin(current_user)

    updated_ids = []
    failed_ids = []

    for curriculum_id in request.curriculum_ids:
        try:
            await curriculum_service.update_curriculum(
                curriculum_id=curriculum_id,
                owner_id=None,  # Admin은 소유자 체크 안함
                role=current_user.role,
                title=request.title,
                visibility=request.visibility,
            )
            updated_ids.append(curriculum_id)
        except Exception as e:
            failed_ids.append({"id": curriculum_id, "error": str(e)})

    return BulkUpdateCurriculumsResponse(
        updated_count=len(updated_ids),
        updated_ids=updated_ids,
        failed_count=len(failed_ids),
        failed_items=failed_ids,
    )


@router.delete("/bulk/users", status_code=200, response_model=BulkDeleteUsersResponse)
@inject
async def bulk_delete_users(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    request: BulkDeleteUsersRequest,
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    """여러 사용자 일괄 삭제"""
    assert_admin(current_user)

    print(request.user_ids)

    deleted_ids = []
    failed_ids = []

    for user_id in request.user_ids:
        try:
            # 자기 자신은 삭제할 수 없도록 체크
            if user_id == current_user.id:
                failed_ids.append({"id": user_id, "error": "Cannot delete yourself"})
                continue

            await user_service.delete_user(user_id)
            deleted_ids.append(user_id)
        except Exception as e:
            failed_ids.append({"id": user_id, "error": str(e)})

    return BulkDeleteUsersResponse(
        deleted_count=len(deleted_ids),
        deleted_ids=deleted_ids,
        failed_count=len(failed_ids),
        failed_items=failed_ids,
    )
