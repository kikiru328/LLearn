from domain.repositories.user_repository import UserRepository
from domain.services.password_service import PasswordService
from domain.value_objects.email import Email
from usecase.dto.user_dto import LoginUseCaseRequest, LoginUseCaseResponse


class LoginUserUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        password_service: PasswordService
    ):
        self.user_repository = user_repository
        self.password_service = password_service
        
    async def execute(self, request: LoginUseCaseRequest) -> LoginUseCaseResponse:
        email = Email(request.email)
        user = await self.user_repository.find_by_email(email)
        if not user:
            raise ValueError("존재하지 않는 사용자입니다")
            
        is_valid = self.password_service.verify_password(
            request.password, 
            str(user.hashed_password)
        )
        if not is_valid:
            raise ValueError("비밀번호가 틀렸습니다")
            
        # JWT 토큰 생성 (일단 mock)
        access_token = f"mock_token_{user.id}"

        return LoginUseCaseResponse(
            user_id=user.id,
            email=str(user.email),
            nickname=user.nickname,
            access_token=access_token
        )