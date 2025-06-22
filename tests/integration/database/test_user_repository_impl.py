import pytest
from uuid import uuid4
from sqlalchemy.orm import sessionmaker
from infrastructure.database.config import engine
from infrastructure.database.base import Base
from infrastructure.database.repositories.user_repository_impl import UserRepositoryImpl
from domain.entities.user import User
from domain.value_objects.email import Email
from domain.value_objects.password import Password


class TestUserRepositoryImpl:
    """User Repository 통합 테스트 - 실제 DB 사용"""

    # 테스트용 해시된 비밀번호 (bcrypt로 "password123" 해시한 값)
    TEST_HASHED_PASSWORD = "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj5mIlz7PGuy"

    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        """각 테스트 전후 DB 초기화"""
        Base.metadata.create_all(bind=engine)

        SessionLocal = sessionmaker(bind=engine)
        self.session = SessionLocal()
        self.repository = UserRepositoryImpl(self.session)

        yield

        self.session.close()
        Base.metadata.drop_all(bind=engine)

    @pytest.mark.asyncio  # ← 추가
    async def test_save_and_find_by_id(self):  # ← async 추가
        """사용자 저장 후 ID로 조회"""
        # Given: 해시된 비밀번호로 사용자 생성
        user = User(
            email=Email("test@test.com"),
            nickname="테스트유저",
            hashed_password=Password(self.TEST_HASHED_PASSWORD),
            is_active=True,
            is_admin=False
        )

        # When
        saved_user = await self.repository.save(user)  # ← await 추가

        # Then
        found_user = await self.repository.find_by_id(saved_user.id)  # ← await 추가

        assert found_user is not None
        assert found_user.email.value == "test@test.com"
        assert found_user.nickname == "테스트유저"
        assert isinstance(found_user.email, Email)
        assert isinstance(found_user.hashed_password, Password)

    @pytest.mark.asyncio  # ← 추가
    async def test_save_and_find_by_email(self):  # ← async 추가
        """사용자 저장 후 이메일로 조회"""
        # Given
        user = User(
            email=Email("email@test.com"),
            nickname="이메일테스트",
            hashed_password=Password(self.TEST_HASHED_PASSWORD)
        )

        # When
        await self.repository.save(user)  # ← await 추가

        # Then
        found_user = await self.repository.find_by_email("email@test.com")  # ← await 추가

        assert found_user is not None
        assert found_user.email.value == "email@test.com"
        assert found_user.nickname == "이메일테스트"

    @pytest.mark.asyncio  # ← 추가
    async def test_find_nonexistent_user_returns_none(self):  # ← async 추가
        """존재하지 않는 사용자 조회시 None 반환"""
        # When
        found_user = await self.repository.find_by_id(uuid4())  # ← await 추가

        # Then
        assert found_user is None

    @pytest.mark.asyncio  # ← 추가
    async def test_delete_user(self):  # ← async 추가
        """사용자 삭제"""
        # Given
        user = User(
            email=Email("delete@test.com"),
            nickname="삭제테스트",
            hashed_password=Password(self.TEST_HASHED_PASSWORD)
        )
        saved_user = await self.repository.save(user)  # ← await 추가

        # When
        result = await self.repository.delete(saved_user.id)  # ← await 추가

        # Then
        assert result is True
        found_user = await self.repository.find_by_id(saved_user.id)  # ← await 추가
        assert found_user is None

    @pytest.mark.asyncio  # ← 추가
    async def test_domain_entity_conversion(self):  # ← async 추가
        """Domain Entity ↔ SQLAlchemy Model 변환 검증"""
        # Given
        original_user = User(
            email=Email("conversion@test.com"),
            nickname="변환테스트",
            hashed_password=Password(self.TEST_HASHED_PASSWORD),
            is_active=True,
            is_admin=False
        )

        # When
        saved_user = await self.repository.save(original_user)  # ← await 추가
        found_user = await self.repository.find_by_email("conversion@test.com")  # ← await 추가

        # Then
        assert isinstance(found_user.email, Email)
        assert isinstance(found_user.hashed_password, Password)
        assert found_user.email.value == "conversion@test.com"
        assert found_user.is_active == True
        assert found_user.is_admin == False