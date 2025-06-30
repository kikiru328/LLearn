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