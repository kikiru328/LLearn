from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from dependency_injector.wiring import inject, Provide

from common.auth import CurrentUser, get_current_user, Role
from user.application.user_service import UserService
from user.interface.schemas.user_schema import (
    GetUsersPageResponse,
    UpdateUserRoleBody,
    UserResponse,
)
from user.interface.schemas.user_schema import UpdateUserBody, UpdateUserResponse

from DI.containers import Container

router = APIRouter(prefix="/users", tags=["users"])


# ────────────────────────────────────────────────────────────
# 본인용: /users/me
# ────────────────────────────────────────────────────────────


# mypage: 조회
@router.get("/me", response_model=UserResponse)
@inject
async def get_me(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    existing_user = await user_service.get_user_by_id(current_user.id)
    return UserResponse.from_domain(existing_user)


# mypage: 수정
@router.put("/me", response_model=UpdateUserResponse)
@inject
async def updated_me(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    user: UpdateUserBody,
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    updated_user = await user_service.update_user(
        user_id=current_user.id,
        name=user.name,
        password=user.password,
    )
    return UpdateUserResponse.from_domain(updated_user)


# mypage: 삭제
@router.delete("/me", status_code=204)
@inject
async def delete_me(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    await user_service.delete_user(current_user.id)


# ────────────────────────────────────────────────────────────
# 관리자용: /users and /users/{user_id}
# ────────────────────────────────────────────────────────────


def assert_admin(current_user: CurrentUser):
    if current_user.role is not Role.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="관리자만 접근이 가능합니다."
        )


# admin/ 전체 조회
@router.get("", status_code=200, response_model=GetUsersPageResponse)
@inject
async def get_list_users(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    page: int = 1,
    items_per_page: int = 18,
    user_service: UserService = Depends(Provide[Container.user_service]),
):

    assert_admin(current_user)

    total_count, domain_users = await user_service.get_users(page, items_per_page)
    users = [UserResponse.from_domain(u) for u in domain_users]

    return GetUsersPageResponse.from_domain(
        total_count=total_count,
        page=page,
        items_per_page=items_per_page,
        users=users,
    )


# admin/ 유저 조회
@router.get("/{user_id}", status_code=201, response_model=UserResponse)
@inject
async def get_user(
    user_id: str,
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    user_service: UserService = Depends(Provide[Container.user_service]),
):

    assert_admin(current_user)

    existing_user = await user_service.get_user_by_id(user_id)

    return UserResponse.from_domain(existing_user)


# admin/ 수정
@router.put("/{user_id}", status_code=201, response_model=UpdateUserResponse)
@inject
async def update_user_by_admin(
    user_id: str,
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    body: UpdateUserBody,
    user_service: UserService = Depends(Provide[Container.user_service]),
):

    assert_admin(current_user)

    updated_user = await user_service.update_user(
        user_id=user_id,
        name=body.name,
        password=body.password,
    )
    return UpdateUserResponse.from_domain(updated_user)


# admin/ 삭제
@router.delete("/{user_id}", status_code=204)
@inject
async def delete_user_by_admin(
    user_id: str,
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    assert_admin(current_user)
    await user_service.delete_user(user_id)


# admin/ role 수정
@router.patch(
    "/{user_id}/role",
    status_code=200,
    response_model=UserResponse,
)
@inject
async def change_user_role_by_admin(
    user_id: str,
    body: UpdateUserRoleBody,
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    user_service: UserService = Depends(Provide[Container.user_service]),
):

    # validation admin
    assert_admin(current_user)

    updated_user = await user_service.change_role(
        user_id=user_id,
        role=body.role,
    )
    return UserResponse.from_domain(updated_user)
