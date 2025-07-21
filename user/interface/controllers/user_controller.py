from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide
from user.application.user_service import UserService
from user.interface.schemas.user_schema import (
    CreateUserBody,
    CreateUserResponse,
    GetUsersPageResponse,
    UserResponse,
)
from user.interface.schemas.user_schema import UpdateUser, UpdateUserResponse

from DI.containers import Container

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", status_code=201, response_model=CreateUserResponse)
@inject  # dependency inject
async def create_user(
    body: CreateUserBody,
    user_service: UserService = Depends(Provide[Container.user_service]),
):

    created_user = await user_service.create_user(
        name=body.name,
        email=body.email,
        password=body.password,
    )
    return CreateUserResponse.from_domain(created_user)


@router.put("/{user_id}", status_code=201, response_model=UpdateUserResponse)
@inject
async def update_user(
    user_id: str,
    user: UpdateUser,
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    updated_user = await user_service.update_user(
        user_id=user_id,
        name=user.name,
        password=user.password,
    )
    return UpdateUserResponse.from_domain(updated_user)


@router.get("", status_code=200, response_model=GetUsersPageResponse)
@inject
async def get_users(
    page: int = 1,
    items_per_page: int = 18,
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    total_count, domain_users = await user_service.get_users(page, items_per_page)
    users = [UserResponse.from_domain(u) for u in domain_users]

    return GetUsersPageResponse.from_domain(
        total_count=total_count,
        page=page,
        items_per_page=items_per_page,
        users=users,
    )


@router.delete("", status_code=204)
@inject
async def delete_user(
    user_id: str,
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    await user_service.delete_user(user_id)
