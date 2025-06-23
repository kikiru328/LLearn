from typing import List
from uuid import uuid4

import pytest
import pytest_asyncio

from domain.entities.curriculum import Curriculum
from domain.entities.user import User
from domain.entities.week_topic import WeekTopic
from domain.value_objects.email import Email
from domain.value_objects.password import Password
from infrastructure.database.repositories import UserRepositoryImpl
from infrastructure.database.repositories.curriculum_repository_impl import CurriculumRepositoryImpl
from infrastructure.database.repositories.week_topic_repository_impl import WeekTopicRepositoryImpl


class TestWeekTopicRepositoryImpl:

    @pytest_asyncio.fixture
    async def test_user(self, test_session):
        """테스트용 user fixture"""
        unique_id = str(uuid4())
        test_hashed_password = f"$2b$12$LQv3c1yqBWVHxkd0LHAk{unique_id}COYz6TtxMQJqhN8/LewdBPj5mIlz7PGuy"
        user = User(
            email=Email(f"test-{unique_id}@example.com"),
            nickname=f"테스트유저-{unique_id}",
            hashed_password=Password(test_hashed_password)
        )
        user_repository = UserRepositoryImpl(test_session)
        return await user_repository.save(user)

    @pytest_asyncio.fixture
    async def test_curriculum(self, test_session, test_user):
        """테스트용 curriculum 생성 helper method"""
        curriculum = Curriculum(
            user_id=test_user.id,
            title="테스트 커리큘럼",
            goal="테스트 목표",
            duration_weeks=12,
            is_public=False
        )
        curriculum_repository = CurriculumRepositoryImpl(test_session)
        return await curriculum_repository.save(curriculum)

    async def create_additional_curriculum(self, test_session, test_user):
        curriculum = Curriculum(
            user_id=test_user.id,
            title="테스트 커리큘럼 2",
            goal="테스트 목표 2",
            duration_weeks=12,
            is_public=False
        )
        curriculum_repository = CurriculumRepositoryImpl(test_session)
        return await curriculum_repository.save(curriculum)

    @pytest.mark.asyncio
    async def test_save_and_find_by_id(self, test_session, test_curriculum):
        repository = WeekTopicRepositoryImpl(test_session)
        week_topic = WeekTopic(
            curriculum_id=test_curriculum.id,
            week_number=1,
            title="1주차",
            description="첫 번째 주",
            learning_goals=["목표1", "목표2"]
        )
        saved_week_topic = await repository.save(week_topic)
        found_week_topic = await repository.find_by_id(week_topic_id=saved_week_topic.id)

        assert found_week_topic is not None
        assert found_week_topic.curriculum_id == test_curriculum.id
        assert found_week_topic.week_number == 1
        assert found_week_topic.title == "1주차"
        assert found_week_topic.description == "첫 번째 주"
        assert found_week_topic.learning_goals == ["목표1", "목표2"]

    @pytest.mark.asyncio
    async def test_save_and_find_by_curriculum_id(self, test_session, test_curriculum):
        repository = WeekTopicRepositoryImpl(test_session)
        week_topic = WeekTopic(
            curriculum_id=test_curriculum.id,
            week_number=1,
            title="1주차",
            description="첫 번째 주",
            learning_goals=["목표1", "목표2"]
        )
        await repository.save(week_topic)
        found_week_topics: List[WeekTopic] = await repository.find_by_curriculum_id(curriculum_id=week_topic.curriculum_id)
        assert len(found_week_topics) == 1
        found_week_topic = found_week_topics[0]
        assert found_week_topic is not None
        assert found_week_topic.curriculum_id == test_curriculum.id
        assert found_week_topic.week_number == 1
        assert found_week_topic.title == "1주차"
        assert found_week_topic.description == "첫 번째 주"
        assert len(found_week_topic.learning_goals) == 2
        assert found_week_topic.learning_goals[0] == "목표1"

    @pytest.mark.asyncio
    async def test_save_and_find_by_curriculum_and_week(self, test_session, test_curriculum):
        repository = WeekTopicRepositoryImpl(test_session)
        week_topic = WeekTopic(
            curriculum_id=test_curriculum.id,
            week_number=1,
            title="1주차",
            description="첫 번째 주",
            learning_goals=["목표1", "목표2"]
        )
        await repository.save(week_topic)
        found_week_topic = await repository.find_by_curriculum_and_week(curriculum_id=test_curriculum.id,
                                                                        week_number=week_topic.week_number)
        assert found_week_topic is not None
        assert found_week_topic.curriculum_id == test_curriculum.id
        assert found_week_topic.week_number == 1
        assert found_week_topic.title == "1주차"
        assert found_week_topic.description == "첫 번째 주"
        assert len(found_week_topic.learning_goals) == 2
        assert found_week_topic.learning_goals[1] == "목표2"

    @pytest.mark.asyncio
    async def test_save_and_find_all(self, test_session, test_user, test_curriculum):
        repository = WeekTopicRepositoryImpl(test_session)
        test_curriculum_1 = test_curriculum
        week_topic_1 = WeekTopic(
            curriculum_id=test_curriculum_1.id,
            week_number=1,
            title="1주차",
            description="첫 번째 주",
            learning_goals=["목표1", "목표2"]
        )
        await repository.save(week_topic_1)
        test_curriculum_2 = await self.create_additional_curriculum(test_session, test_user)
        week_topic_2 = WeekTopic(
            curriculum_id=test_curriculum_2.id,
            week_number=1,
            title="2주차",
            description="두 번째 주",
            learning_goals=["목표3", "목표4", "목표5"]
        )
        await repository.save(week_topic_2)
        found_week_topics: List[WeekTopic] = await repository.find_all()
        assert len(found_week_topics) == 2
        found_week_topic_1 = found_week_topics[0]
        found_week_topic_2 = found_week_topics[1]
        assert found_week_topic_1.title == "1주차"
        assert len(found_week_topic_2.learning_goals) == 3

    @pytest.mark.asyncio
    async def test_save_and_delete(self, test_session, test_curriculum):
        repository = WeekTopicRepositoryImpl(test_session)
        week_topic = WeekTopic(
            curriculum_id=test_curriculum.id,
            week_number=1,
            title="1주차",
            description="첫 번째 주",
            learning_goals=["목표1", "목표2"]
        )
        saved_week_topic = await repository.save(week_topic)
        result = await repository.delete(week_topic_id=saved_week_topic.id)
        assert result is True
        found_week_topic = await repository.find_by_id(week_topic_id=saved_week_topic.id)
        assert found_week_topic is None

    @pytest.mark.asyncio
    async def test_domain_entity_conversion(self, test_session, test_curriculum):
        repository = WeekTopicRepositoryImpl(test_session)
        original_week_topic = WeekTopic(
            curriculum_id=test_curriculum.id,
            week_number=1,
            title="1주차",
            description="첫 번째 주",
            learning_goals=["목표1", "목표2"]
        )
        await repository.save(original_week_topic)
        found_week_topics = await repository.find_by_curriculum_id(curriculum_id=test_curriculum.id)
        found_week_topic = found_week_topics[0]
        assert isinstance(found_week_topic, WeekTopic)
        assert found_week_topic.curriculum_id == test_curriculum.id
        assert found_week_topic.week_number == 1
        assert found_week_topic.title == "1주차"
        assert found_week_topic.description == "첫 번째 주"
        assert len(found_week_topic.learning_goals) == 2
        assert found_week_topic.learning_goals[0] == "목표1"
        assert found_week_topic.id is not None
