from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from dependency_injector.wiring import inject, Provide

from common.auth import CurrentUser, get_current_user, Role

from admin.interface.schemas.admin_user_schema import (
    AdminGetUserResponse,
    AdminGetUsersPageResponse,
    AdminUpdateUserResponse,
    AdminUpdateUserBody,
)

from DI.containers import Container
from user.application.user_service import UserService


router = APIRouter(prefix="/admins/users", tags=["admins/users"])


def assert_admin(current_user: CurrentUser) -> None:
    if current_user.role != Role.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="관리자만 접근이 가능합니다."
        )


@router.get("/", status_code=200, response_model=AdminGetUsersPageResponse)
@inject
async def get_users_page_for_admin(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    page: int = 1,
    items_per_page: int = 10,
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    # 관리자 권한 확인
    assert_admin(current_user)

    total_count, domain_users = await user_service.get_users(page, items_per_page)
    users: list[AdminGetUserResponse] = [
        AdminGetUserResponse.from_domain(u) for u in domain_users
    ]

    return AdminGetUsersPageResponse.from_domain(
        total_count=total_count,
        page=page,
        items_per_page=items_per_page,
        users=users,
    )


@router.get("/{user_id}", status_code=200, response_model=AdminGetUserResponse)
@inject
async def get_user_by_id_for_admin(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    user_id: str,
    user_service: UserService = Depends(Provide[Container.user_service]),
):

    # 관리자 권한 확인
    assert_admin(current_user)

    existsing_user = await user_service.get_user_by_id(user_id)
    return AdminGetUserResponse.from_domain(existsing_user)


# admin/ 수정
@router.patch("/{user_id}", status_code=200, response_model=AdminUpdateUserResponse)
@inject
async def update_user_by_admin(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    user_id: str,
    body: AdminUpdateUserBody,
    user_service: UserService = Depends(Provide[Container.user_service]),
) -> AdminUpdateUserResponse:

    assert_admin(current_user)

    updated_user = await user_service.update_user(
        user_id=user_id,
        name=body.name,
        password=body.password,
        role=body.role,
    )
    return AdminUpdateUserResponse.from_domain(updated_user)


@router.delete("/{user_id}", status_code=204)
@inject
async def delete_user_by_admin(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    user_id: str,
    user_service: UserService = Depends(Provide[Container.user_service]),
):

    assert_admin(current_user)

    await user_service.delete_user(user_id)
