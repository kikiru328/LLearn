from typing import Annotated
from fastapi import APIRouter, Depends, status
from dependency_injector.wiring import inject, Provide

from common.auth import CurrentUser, get_current_user
from user.application.user_service import UserService
from user.interface.schemas.user_schema import (
    GetUserResponse,
    GetUsersPageResponse,
    UpdateUserBody,
    UpdateUserResponse,
)

from DI.containers import Container

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=GetUserResponse)
@inject
async def get_me(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    existing_user = await user_service.get_user_by_id(current_user.id)
    return GetUserResponse.from_domain(existing_user)


# mypage: 수정
@router.put("/me", response_model=UpdateUserResponse)
@inject
async def update_me(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    user: UpdateUserBody,
    user_service: UserService = Depends(Provide[Container.user_service]),
) -> UpdateUserResponse:
    updated_user = await user_service.update_user(
        user_id=current_user.id,
        name=user.name,
        password=user.password,
    )
    return UpdateUserResponse.from_domain(updated_user)


# mypage: 삭제
@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_me(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    await user_service.delete_user(current_user.id)


# admin/ 전체 조회
@router.get("", status_code=200, response_model=GetUsersPageResponse)
@inject
async def get_users_for_social(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    page: int = 1,
    items_per_page: int = 18,
    user_service: UserService = Depends(Provide[Container.user_service]),
):

    total_count, domain_users = await user_service.get_users(page, items_per_page)
    users: list[GetUserResponse] = [
        GetUserResponse.from_domain(u) for u in domain_users
    ]

    return GetUsersPageResponse.from_domain(
        total_count=total_count,
        page=page,
        items_per_page=items_per_page,
        users=users,
    )


# admin/ 유저 조회
@router.get("/{user_name}", status_code=200, response_model=GetUserResponse)
@inject
async def get_user_by_name(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    user_name: str,
    user_service: UserService = Depends(Provide[Container.user_service]),
):

    existing_user = await user_service.get_user_by_name(user_name)

    return GetUserResponse.from_domain(existing_user)
