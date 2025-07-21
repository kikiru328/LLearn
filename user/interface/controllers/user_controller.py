from fastapi import APIRouter, Depends

from db.session import get_db
from user.application.user_service import UserService
from user.infra.repository.user_repo import UserRepository
from user.interface.schemas.user_schema import CreateUserBody, CreateUserResponse
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/users", tags=["users"])


def get_user_service(
    db: AsyncSession = Depends(get_db),
) -> UserService:
    repo = UserRepository(db)
    return UserService(user_repo=repo)


@router.post("", status_code=201, response_model=CreateUserResponse)
async def create_user(
    user: CreateUserBody,
    user_service: UserService = Depends(get_user_service),
):

    created_user = await user_service.create_user(
        name=user.name,
        email=user.email,
        password=user.password,
    )
    return CreateUserResponse.from_domain(created_user)
