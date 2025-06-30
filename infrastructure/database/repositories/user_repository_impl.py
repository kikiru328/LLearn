from typing import Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timezone

from domain.entities.user import User
from domain.value_objects.email import Email
from domain.value_objects.password import Password
from domain.repositories.user_repository import UserRepository  # 인터페이스
from infrastructure.database.models.user_model import UserModel


class UserRepositoryImpl(UserRepository):
    """User Repository SQLAlchemy 구현체"""

    def __init__(self, session: AsyncSession):
        """
        Args:
            session: SQLAlchemy 세션 (의존성 주입)
        """
        self.session = session

    async def save(self, user: User) -> User:
        """
        사용자 저장

        Args:
            user: Domain User Entity

        Returns:
            User: 저장된 사용자 엔티티
        """
        # 1. Domain Entity → SQLAlchemy Model 변환
        user_model = UserModel(
            id=str(user.id),  # UUID → str
            email=user.email.value,  # Email VO → str
            nickname=user.nickname,
            hashed_password=str(user.hashed_password),  # Password VO → str
            is_active=user.is_active,
            is_admin=user.is_admin,
            created_at=user.created_at,
            updated_at=user.updated_at
        )

        # 2. DB에 저장
        self.session.add(user_model) # 메모리에 객체 추가(DB접근X)
        await self.session.commit() # 실제 DB 작성, DB 접근 O
        await self.session.refresh(user_model)  # DB에서 생성된 값들 다시 로드

        # 3. SQLAlchemy Model → Domain Entity 변환
        return self._model_to_entity(user_model)

    async def find_by_id(self, user_id: UUID) -> Optional[User]:
        """ID로 사용자 찾기"""
        # SELECT * FROM users WHERE id = 'uuid값'
        stmt = select(UserModel).where(UserModel.id == str(user_id))
        # query 실행 -> DB 접근
        result = await self.session.execute(stmt)
        #scalar_one_or_none(): 결과가 1개면 반환, 0개면 None, 2개 이상이면 에러
        user_model = result.scalar_one_or_none()

        if user_model is None:
            return None
        return self._model_to_entity(user_model)

    async def find_by_email(self, email: Email) -> Optional[User]:
        """이메일로 사용자 찾기"""
        stmt = select(UserModel).where(UserModel.email == email.value)
        result = await self.session.execute(stmt)
        user_model = result.scalar_one_or_none()

        if user_model is None:
            return None

        return self._model_to_entity(user_model)

    async def delete(self, user_id: UUID) -> bool:
        """사용자 삭제"""
        stmt = select(UserModel).where(UserModel.id == str(user_id))
        result = await self.session.execute(stmt)
        user_model = result.scalar_one_or_none()

        if user_model is None:
            return False

        await self.session.delete(user_model)
        await self.session.commit()
        return True

    async def exists_by_email(self, email: Email) -> bool:
        """이메일로 사용자 존재 여부 확인"""
        stmt = select(UserModel).where(UserModel.email == email.value)
        result = await self.session.execute(stmt)
        user_model = result.scalar_one_or_none()
        return user_model is not None

    async def update_password(self, user_id: UUID, new_password: Password) -> bool:
        """사용자 비밀번호 업데이트"""
        stmt = select(UserModel).where(UserModel.id == str(user_id))
        result = await self.session.execute(stmt)
        user_model = result.scalar_one_or_none()

        if user_model is None:
            return False

        user_model.hashed_password = str(new_password)
        user_model.updated_at = datetime.now(timezone.utc)
        await self.session.commit()
        return True

    def _model_to_entity(self, user_model: UserModel) -> User:
        """SQLAlchemy Model → Domain Entity 변환"""
        from domain.value_objects.email import Email
        from domain.value_objects.password import Password
        from uuid import UUID

        return User(
            id=UUID(user_model.id),
            email=Email(user_model.email),
            nickname=user_model.nickname,
            hashed_password=Password(user_model.hashed_password),
            is_active=user_model.is_active,
            is_admin=user_model.is_admin,
            created_at=user_model.created_at,
            updated_at=user_model.updated_at
        )