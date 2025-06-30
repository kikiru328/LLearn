
from domain.entities.user import User
from domain.repositories.user_repository import UserRepository
from domain.services.password_service import PasswordService
from domain.value_objects.email import Email
from domain.value_objects.password import Password
from usecase.dto.user_dto import CreateUserUseCaseRequest, CreateUserUseCaseResponse



class CreateUserUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        password_service: PasswordService
    ):
        self.user_repository = user_repository
        self.password_service = password_service
        
    async def execute(self, request: CreateUserUseCaseRequest) -> CreateUserUseCaseResponse:
        
        # 이메일 중복 검사
        email = Email(request.email)
        existing_user = await self.user_repository.find_by_email(email)
        if existing_user:
            raise ValueError(f"이미 존재하는 이메일입니다: {request.email}")
            
        # 비밀번호 해싱
        hashed_pwd = self.password_service.hash_password(request.password)
        password_vo = Password(hashed_value=hashed_pwd)
        
        # User Entity 생성
        user = User(
            email=email,
            nickname=request.nickname,
            hashed_password=password_vo
        )
        
        # 저장
        saved_user = await self.user_repository.save(user)
        
        # 응답 반환
        
        return CreateUserUseCaseResponse(
            id=saved_user.id,
            email=str(saved_user.email),  # Email VO → string
            nickname=saved_user.nickname,
            is_active=saved_user.is_active,
            is_admin=saved_user.is_admin,
            created_at=saved_user.created_at,
            updated_at=saved_user.updated_at
        )

        