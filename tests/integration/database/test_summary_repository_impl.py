from dataclasses import dataclass
from typing import List
from uuid import uuid4

import pytest
import pytest_asyncio

from domain.entities.curriculum import Curriculum
from domain.entities.summary import Summary
from domain.entities.user import User
from domain.entities.week_topic import WeekTopic
from domain.value_objects.email import Email
from domain.value_objects.password import Password
from infrastructure.database.repositories import UserRepositoryImpl
from infrastructure.database.repositories.curriculum_repository_impl import CurriculumRepositoryImpl
from infrastructure.database.repositories.summary_repository_impl import SummaryRepositoryImpl
from infrastructure.database.repositories.week_topic_repository_impl import WeekTopicRepositoryImpl

@dataclass
class DataTest:
    test_user: User
    test_curriculum: Curriculum
    test_week_topic: WeekTopic

class TestSummaryRepositoryImpl:

    @pytest_asyncio.fixture
    async def repository(self, test_session):
        return SummaryRepositoryImpl(test_session)


    @pytest_asyncio.fixture
    async def test_data(self, test_session) -> DataTest:
        unique_id = str(uuid4())
        test_user = await UserRepositoryImpl(test_session).save(
            User(
                email=Email(f"test-{unique_id}@example.com"),
                nickname=f"유저-{unique_id}",
                hashed_password=Password(f"$2b$12$HASHED{unique_id}")
            )
        )
        test_curriculum = await CurriculumRepositoryImpl(test_session).save(
            Curriculum(
                user_id=test_user.id,
                title="테스트 커리큘럼",
                goal="목표입니다",
                duration_weeks=4,
                is_public=False
            )
        )
        test_week_topic = await WeekTopicRepositoryImpl(test_session).save(
            WeekTopic(
                curriculum_id=test_curriculum.id,
                week_number=1,
                title="1주차",
                description="설명입니다",
                learning_goals=["목표1", "목표2"]
            )
        )
        return DataTest(test_user=test_user,
                        test_curriculum=test_curriculum,
                        test_week_topic=test_week_topic)

    async def create_additional_week_topic(self, test_session, test_curriculum, week_number: int = 2) -> WeekTopic:
        return await WeekTopicRepositoryImpl(test_session).save(
            WeekTopic(
                curriculum_id=test_curriculum.id,
                week_number=week_number,
                title=f"{week_number}주차",
                description=f"{week_number}주차 설명",
                learning_goals=[f"목표{week_number}a", f"목표{week_number}b"]
                )
            )

    @pytest.mark.asyncio
    async def test_save_and_find_by_id(self, repository, test_session, test_data):
        summary = Summary(
            user_id=test_data.test_user.id,
            week_topic_id=test_data.test_week_topic.id,
            content="테스트 요약본",
            is_public=True,
        )
        saved_summary = await repository.save(summary)
        found_summary = await repository.find_by_id(summary_id=saved_summary.id)

        assert found_summary is not None
        assert found_summary.user_id == test_data.test_user.id
        assert found_summary.content == "테스트 요약본"
        assert found_summary.is_public == True

    @pytest.mark.asyncio
    async def test_save_and_find_by_user_id(self, test_session, repository, test_data):
        summary = Summary(
            user_id=test_data.test_user.id,
            week_topic_id=test_data.test_week_topic.id,
            content="테스트 요약본",
            is_public=True,
        )
        await repository.save(summary)
        found_summaries: List[Summary] = await repository.find_by_user_id(user_id=test_data.test_user.id)
        assert len(found_summaries) == 1
        found_summary = found_summaries[0]
        assert found_summary is not None
        assert found_summary.week_topic_id == test_data.test_week_topic.id

    @pytest.mark.asyncio
    async def test_save_and_find_by_week_topic_id(self, test_session, repository, test_data):
        summary = Summary(
            user_id=test_data.test_user.id,
            week_topic_id=test_data.test_week_topic.id,
            content="테스트 요약본",
            is_public=True,
        )
        await repository.save(summary)
        found_summary = await repository.find_by_week_topic_id(week_topic_id=test_data.test_week_topic.id)
        assert found_summary is not None
        assert found_summary.user_id == test_data.test_user.id
        assert found_summary.content == "테스트 요약본"
        assert found_summary.is_public == True

    @pytest.mark.asyncio
    async def test_save_and_find_public_summaries(self, test_session, repository, test_data):
        summary = Summary(
            user_id=test_data.test_user.id,
            week_topic_id=test_data.test_week_topic.id,
            content="테스트 요약본",
            is_public=True,
        )
        await repository.save(summary)
        found_summaries: List[Summary] = await repository.find_public_summaries()
        assert len(found_summaries) == 1
        assert found_summaries[0].content == "테스트 요약본"

    @pytest.mark.asyncio
    async def test_save_and_find_all(self, test_session, repository, test_data):
        summary = Summary(
            user_id=test_data.test_user.id,
            week_topic_id=test_data.test_week_topic.id,
            content="테스트 요약본",
            is_public=True,
        )
        await repository.save(summary)
        week2 = await self.create_additional_week_topic(test_session,
                                                        test_curriculum=test_data.test_curriculum,
                                                        week_number=2)
        summary2 = Summary(
            user_id=test_data.test_user.id,
            week_topic_id=week2.id,
            content="테스트 요약본 2",
            is_public=True,
        )
        await repository.save(summary2)
        found_summaries: List[Summary] = await repository.find_all()
        assert len(found_summaries) == 2
        found_summary2 = found_summaries[1]
        assert found_summary2.content == "테스트 요약본 2"
        assert found_summary2.week_topic_id == week2.id

    @pytest.mark.asyncio
    async def test_save_and_delete(self, test_session, repository, test_data):
        summary = Summary(
            user_id=test_data.test_user.id,
            week_topic_id=test_data.test_week_topic.id,
            content="테스트 요약본",
            is_public=True,
        )
        saved_summary = await repository.save(summary)
        result = await repository.delete(summary_id=saved_summary.id)
        assert result is True
        found_summary = await repository.find_by_id(summary_id=saved_summary.id)
        assert found_summary is None

    @pytest.mark.asyncio
    async def test_domain_entity_conversion(self, test_session, repository, test_data):
        original_summary = Summary(
            user_id=test_data.test_user.id,
            week_topic_id=test_data.test_week_topic.id,
            content="테스트 요약본",
            is_public=True,
        )
        await repository.save(original_summary)
        found_summaries = await repository.find_by_user_id(user_id=test_data.test_user.id)
        found_summary = found_summaries[0]
        assert isinstance(found_summary, Summary)
        assert found_summary.user_id == test_data.test_user.id
        assert found_summary.week_topic_id == test_data.test_week_topic.id
        assert found_summary.content == "테스트 요약본"
        assert found_summary.is_public == True
        assert found_summary.id is not None


