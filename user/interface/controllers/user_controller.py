from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from dependency_injector.wiring import inject, Provide
from fastapi.security import OAuth2PasswordRequestForm
from common.auth import CurrentUser, get_current_user, Role
from user.application.user_service import UserService
from user.interface.schemas.user_schema import (
    CreateUserBody,
    CreateUserResponse,
    GetUsersPageResponse,
    TokenResponse,
    UserResponse,
)
from user.interface.schemas.user_schema import UpdateUserBody, UpdateUserResponse

from DI.containers import Container

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/login", response_model=TokenResponse)
@inject
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    access_token, role = await user_service.login(
        email=form_data.username,
        password=form_data.password,
    )
    return TokenResponse(access_token=access_token, role=role.value)


# 회원가입 (stranger, admin)
@router.post("", status_code=201, response_model=CreateUserResponse)
@inject  # dependency inject
async def create_user(
    user: CreateUserBody,
    user_service: UserService = Depends(Provide[Container.user_service]),
):

    created_user = await user_service.create_user(
        name=user.name,
        email=user.email,
        password=user.password,
    )
    return CreateUserResponse.from_domain(created_user)


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
    print("#############################")
    print(current_user.role)
    print("#############################")
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
