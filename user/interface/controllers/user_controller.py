from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from dependency_injector.wiring import inject, Provide

from common.auth import CurrentUser, get_current_user, Role
from user.application.user_service import UserService
from user.interface.schemas.user_schema import (
    GetUsersPageResponse,
    UserResponse,
)
from user.interface.schemas.user_schema import UpdateUserBody, UpdateUserResponse

from DI.containers import Container

router = APIRouter(prefix="/users", tags=["users"])


# 수정 (user)
@router.put("/{user_id}", status_code=201, response_model=UpdateUserResponse)
@inject
async def update_user(
    # user_id: str,
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


# 전체조회 (admin)
@router.get("", status_code=200, response_model=GetUsersPageResponse)
@inject
async def get_users(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    page: int = 1,
    items_per_page: int = 18,
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    if current_user.role is not Role.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="관리자만 접근이 가능합니다."
        )

    total_count, domain_users = await user_service.get_users(page, items_per_page)
    users = [UserResponse.from_domain(u) for u in domain_users]

    return GetUsersPageResponse.from_domain(
        total_count=total_count,
        page=page,
        items_per_page=items_per_page,
        users=users,
    )


# 삭제 (user, admin)
@router.delete("", status_code=204)
@inject
async def delete_user(
    user_id: str,
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    await user_service.delete_user(user_id)
