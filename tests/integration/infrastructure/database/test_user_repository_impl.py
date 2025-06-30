import bcrypt
import pytest
from uuid import uuid4
from infrastructure.database.repositories.user_repository_impl import UserRepositoryImpl
from domain.entities.user import User
from domain.value_objects.email import Email
from domain.value_objects.password import Password
DUMMY = str(uuid4()).encode()

class TestUserRepositoryImpl:
    """User Repository 통합 테스트 - 실제 DB 사용"""

    # 테스트용 해시된 비밀번호 (bcrypt로 "password123" 해시한 값)\
        

    HASHED_PWD = bcrypt.hashpw(DUMMY, bcrypt.gensalt()).decode()

    @pytest.mark.asyncio
    async def test_save_and_find_by_id(self, test_session):
        """사용자 저장 후 ID로 조회"""
        # Given: 해시된 비밀번호로 사용자 생성
        repository = UserRepositoryImpl(test_session)
        unique_id = str(uuid4())
        user = User(
            email=Email(f"test-{unique_id}@example.com"),
            nickname=f"테스트유저-{unique_id}",
            hashed_password=Password(self.HASHED_PWD),
            is_active=True,
            is_admin=False
        )

        # When
        saved_user = await repository.save(user)

        # Then
        found_user = await repository.find_by_id(saved_user.id)

        assert found_user is not None
        assert found_user.email.value == f"test-{unique_id}@example.com"
        assert found_user.nickname == f"테스트유저-{unique_id}"
        assert isinstance(found_user.email, Email)
        assert isinstance(found_user.hashed_password, Password)

    @pytest.mark.asyncio
    async def test_save_and_find_by_email(self, test_session):
        """사용자 저장 후 이메일로 조회"""
        # Given
        email = Email("email@test.com")
        repository = UserRepositoryImpl(test_session)
        user = User(
            email=email,
            nickname="이메일테스트",
            hashed_password=Password(self.HASHED_PWD)
        )

        # When
        await repository.save(user)

        # Then
        found_user = await repository.find_by_email(email)

        assert found_user is not None
        assert found_user.email.value == "email@test.com"
        assert found_user.nickname == "이메일테스트"

    @pytest.mark.asyncio
    async def test_find_nonexistent_user_returns_none(self, test_session):
        """존재하지 않는 사용자 조회시 None 반환"""
        # When
        repository = UserRepositoryImpl(test_session)
        found_user = await repository.find_by_id(uuid4())

        # Then
        assert found_user is None

    @pytest.mark.asyncio
    async def test_delete_user(self, test_session):
        """사용자 삭제"""
        # Given
        repository = UserRepositoryImpl(test_session)
        user = User(
            email=Email("delete@test.com"),
            nickname="삭제테스트",
            hashed_password=Password(self.HASHED_PWD)
        )
        saved_user = await repository.save(user)

        # When
        result = await repository.delete(saved_user.id)

        # Then
        assert result is True
        found_user = await repository.find_by_id(saved_user.id)
        assert found_user is None

    @pytest.mark.asyncio
    async def test_domain_entity_conversion(self, test_session):
        """Domain Entity ↔ SQLAlchemy Model 변환 검증"""
        # Given
        repository = UserRepositoryImpl(test_session)
        email = Email("conversion@test.com")
        original_user = User(
            email=email,
            nickname="변환테스트",
            hashed_password=Password(self.HASHED_PWD),
            is_active=True,
            is_admin=False
        )

        # When
        await repository.save(original_user)
        found_user = await repository.find_by_email(email)

        # Then
        assert isinstance(found_user.email, Email)
        assert isinstance(found_user.hashed_password, Password)
        assert found_user.email.value == "conversion@test.com"
        assert found_user.is_active == True
        assert found_user.is_admin == False
