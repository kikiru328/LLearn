from fastapi import APIRouter, status

from app.api.deps import CreateUserUseCaseDep
from app.schemas.user import CreateUserRequest, UserResponse
from usecase.dto.user_dto import CreateUserUseCaseRequest, GetUserProfileRequest
from usecase.user.get_user_profile import GetUserProfileUseCase


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(
    request: CreateUserRequest,
    usecase: CreateUserUseCaseDep,  # API 요청  # 의존성 주입
) -> UserResponse:  # API 응답

    usecase_request = CreateUserUseCaseRequest(
        email=str(request.email),
        nickname=request.nickname,
        password=request.password,
    )

    usecase_response = await usecase.execute(usecase_request)

    return UserResponse(
        id=usecase_response.id,
        email=usecase_response.email,
        nickname=usecase_response.nickname,
        is_active=usecase_response.is_active,
        is_admin=usecase_response.is_admin,
        created_at=usecase_response.created_at,
        updated_at=usecase_response.updated_at,
    )
