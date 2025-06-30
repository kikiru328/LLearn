from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class CreateUserUseCaseRequest:
    """CreateUserUseCase 입력 DTO"""
    email: str
    nickname: str
    password: str


@dataclass
class CreateUserUseCaseResponse:
    """CreateUserUseCase 출력 DTO"""
    id: UUID
    email: str
    nickname: str
    is_active: bool
    is_admin: bool
    created_at: datetime
    updated_at: datetime
    
@dataclass
class LoginUseCaseRequest:
    """LoginUseCase 입력 DTO"""
    email: str
    password: str


@dataclass
class LoginUseCaseResponse:
    """LoginUseCase 출력 DTO"""
    user_id: UUID
    email: str
    nickname: str
    access_token: str  # JWT 토큰
    

@dataclass
class GetUserProfileRequest:
    """사용자 프로필 조회 요청"""
    user_id: UUID

@dataclass
class GetUserProfileResponse:
    """사용자 프로필 조회 응답"""
    id: UUID
    email: str
    nickname: str
    created_at: datetime
    updated_at: datetime
    
    # 통계 정보 (선택)
    curriculum_count: int = 0  # 만든 커리큘럼 수
    summary_count: int = 0     # 작성한 요약 수
            