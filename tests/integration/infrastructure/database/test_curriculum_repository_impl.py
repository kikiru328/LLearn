from typing import List
from uuid import uuid4

import bcrypt
import pytest
import pytest_asyncio

from domain.entities.curriculum import Curriculum
from domain.entities.user import User
from domain.value_objects.email import Email
from domain.value_objects.password import Password
from infrastructure.database.repositories import UserRepositoryImpl
from infrastructure.database.repositories.curriculum_repository_impl import CurriculumRepositoryImpl

DUMMY = b"dummy_value"
HASHED_PWD = bcrypt.hashpw(DUMMY, bcrypt.gensalt()).decode()

class TestCurriculumRepositoryImpl:

    @pytest_asyncio.fixture
    async def test_user(self, test_session):
        """테스트용 user fixture"""
        unique_id = str(uuid4())
        test_hashed_password = f"{HASHED_PWD}{unique_id}"
        user = User(
            email=Email(f"test-{unique_id}@example.com"),
            nickname=f"테스트유저-{unique_id}",
            hashed_password=Password(test_hashed_password)
        )
        user_repository = UserRepositoryImpl(test_session)
        return await user_repository.save(user)

    async def create_additional_user(self, test_session):
        """추가 사용자 생성용 helper method"""
        unique_id = str(uuid4())
        test_hashed_password = f"{HASHED_PWD}{unique_id}"
        user = User(
            email=Email(f"test-{unique_id}@example.com"),
            nickname=f"테스트유저-{unique_id}",
            hashed_password=Password(test_hashed_password)
        )
        user_repository = UserRepositoryImpl(test_session)
        return await user_repository.save(user)

    @pytest.mark.asyncio
    async def test_save_and_find_by_id(self, test_session, test_user):
        repository = CurriculumRepositoryImpl(test_session)
        curriculum = Curriculum(
            user_id=test_user.id,
            title="테스트 커리큘럼",
            goal="python master",
            duration_weeks=12,
            is_public=False
        )
        # saved
        saved_curriculum = await repository.save(curriculum)
        found_curriculum = await repository.find_by_id(curriculum_id=saved_curriculum.id)

        assert found_curriculum is not None
        assert found_curriculum.user_id == test_user.id
        assert found_curriculum.title == "테스트 커리큘럼"
        assert found_curriculum.goal == "python master"
        assert found_curriculum.duration_weeks == 12
        assert found_curriculum.is_public == False

    @pytest.mark.asyncio
    async def test_save_and_find_by_user_id(self, test_session, test_user):
        repository = CurriculumRepositoryImpl(test_session)
        curriculum = Curriculum(
            user_id=test_user.id,
            title="테스트 커리큘럼",
            goal="python master",
            duration_weeks=12,
            is_public=False
        )
        await repository.save(curriculum)
        found_curriculums: List[Curriculum] = await repository.find_by_user_id(user_id=test_user.id)
        assert len(found_curriculums) == 1
        found_curriculum = found_curriculums[0]
        assert found_curriculum is not None
        assert found_curriculum.user_id == test_user.id
        assert found_curriculum.title == "테스트 커리큘럼"
        assert found_curriculum.goal == "python master"
        assert found_curriculum.duration_weeks == 12

    @pytest.mark.asyncio
    async def test_save_and_find_public_curriculums(self, test_session, test_user):
        repository = CurriculumRepositoryImpl(test_session)
        curriculum = Curriculum(
            user_id=test_user.id,
            title="테스트 커리큘럼",
            goal="python master",
            duration_weeks=12,
            is_public=True # 하나라도 찾아야 됨
        )
        await repository.save(curriculum)
        found_curriculums: List[Curriculum] = await repository.find_public_curriculums()
        assert len(found_curriculums) == 1
        found_curriculum = found_curriculums[0]
        assert found_curriculum is not None
        assert found_curriculum.is_public == True
        assert found_curriculum.user_id == test_user.id
        assert found_curriculum.title == "테스트 커리큘럼"
        assert found_curriculum.goal == "python master"
        assert found_curriculum.duration_weeks == 12

    @pytest.mark.asyncio
    async def test_save_and_find_all(self, test_session, test_user):
        test_user1 = test_user
        test_user2 = await self.create_additional_user(test_session)
        repository = CurriculumRepositoryImpl(test_session)
        curriculum_1 = Curriculum(
                user_id=test_user1.id,
                title="테스트 커리큘럼 1",
                goal="python master 1",
                duration_weeks=12,
                is_public=False
        )
        await repository.save(curriculum=curriculum_1)
        curriculum_2 = Curriculum(
            user_id=test_user2.id,
            title="테스트 커리큘럼 2",
            goal="python master 2",
            duration_weeks=12,
            is_public=False
        )
        await repository.save(curriculum=curriculum_2)
        found_curriculums: List[Curriculum] = await repository.find_all()
        assert len(found_curriculums) == 2
        found_curriculum_1 = found_curriculums[0]
        found_curriculum_2 = found_curriculums[1]
        assert found_curriculum_1.title == "테스트 커리큘럼 1"
        assert found_curriculum_2.goal == "python master 2"

    @pytest.mark.asyncio
    async def test_save_and_delete(self, test_session, test_user):
        repository = CurriculumRepositoryImpl(test_session)
        curriculum = Curriculum(
            user_id=test_user.id,
            title="테스트 커리큘럼",
            goal="python master",
            duration_weeks=12,
            is_public=True
        )
        saved_curriculum = await repository.save(curriculum)
        result = await repository.delete(curriculum_id=saved_curriculum.id) #deleted

        assert result is True
        found_curriculum = await repository.find_by_id(curriculum_id=saved_curriculum.id)
        assert found_curriculum is None

    @pytest.mark.asyncio
    async def test_domain_entity_conversion(self, test_session, test_user):
        """Domain Entity ↔ SQLAlchemy Model 변환 검증"""
        repository = CurriculumRepositoryImpl(test_session)
        original_curriculum = Curriculum(
            user_id=test_user.id,
            title="테스트 커리큘럼",
            goal="python master",
            duration_weeks=12,
            is_public=True
        )

        await repository.save(original_curriculum)
        found_curriculums = await repository.find_by_user_id(user_id=test_user.id)
        found_curriculum = found_curriculums[0]

        assert isinstance(found_curriculum, Curriculum)  # ← 타입 확인
        assert found_curriculum.user_id == test_user.id
        assert found_curriculum.title == "테스트 커리큘럼"
        assert found_curriculum.goal == "python master"
        assert found_curriculum.duration_weeks == 12
        assert found_curriculum.is_public == True
        assert found_curriculum.id is not None
