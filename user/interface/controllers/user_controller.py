from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide
from user.application.user_service import UserService
from user.interface.schemas.user_schema import CreateUserBody, CreateUserResponse

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
