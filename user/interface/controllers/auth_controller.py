from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from dependency_injector.wiring import inject, Provide
from user.application.auth_service import AuthService
from user.domain.entity.user import User
from user.interface.schemas.auth_schema import SignUpBody, SignUpResponse, TokenResponse
from DI.containers import Container

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=SignUpResponse)
@inject
async def signup(
    body: SignUpBody,
    auth_service: AuthService = Depends(Provide[Container.auth_service]),
):
    created_user: User = await auth_service.signup(
        name=body.name,
        email=body.email,
        password=body.password,  # process in auth_service
    )
    return SignUpResponse.from_domain(created_user)


@router.post("/login", response_model=TokenResponse)
@inject
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: AuthService = Depends(Provide[Container.auth_service]),
):
    access_token, role = await auth_service.login(
        email=form_data.username,
        password=form_data.password,
    )
    return TokenResponse(access_token=access_token, role=role.value)
