from dataclasses import dataclass
from typing import List
from uuid import uuid4
import pytest
import pytest_asyncio
from domain.entities.curriculum import Curriculum
from domain.entities.feedback import Feedback
from domain.entities.summary import Summary
from domain.entities.user import User
from domain.entities.week_topic import WeekTopic
from domain.value_objects.email import Email
from domain.value_objects.password import Password
from infrastructure.database.repositories import UserRepositoryImpl
from infrastructure.database.repositories.curriculum_repository_impl import CurriculumRepositoryImpl
from infrastructure.database.repositories.feedback_repository_impl import FeedbackRepositoryImpl
from infrastructure.database.repositories.summary_repository_impl import SummaryRepositoryImpl
from infrastructure.database.repositories.week_topic_repository_impl import WeekTopicRepositoryImpl


@dataclass
class DataTest:
    test_user: User
    test_curriculum: Curriculum
    test_week_topic: WeekTopic
    test_summary: Summary

class TestFeedbackRepositoryImpl:

    @pytest_asyncio.fixture
    async def repository(self, test_session):
        return FeedbackRepositoryImpl(test_session)

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
        test_summary = await SummaryRepositoryImpl(test_session).save(
            Summary(
                user_id=test_user.id,
                week_topic_id=test_week_topic.id,
                content="테스트 요약본",
                is_public=True,
            )
        )
        return DataTest(test_user=test_user,
                        test_curriculum=test_curriculum,
                        test_week_topic=test_week_topic,
                        test_summary=test_summary)

    async def create_additional_summary_by_week(self, test_session, test_data, week_number: int = 2) -> Summary:
        new_week_topic = await WeekTopicRepositoryImpl(test_session).save(
            WeekTopic(
                curriculum_id=test_data.test_curriculum.id,
                week_number=week_number,
                title=f"{week_number}주차",
                description=f"{week_number}주차 설명",
                learning_goals=[f"목표{week_number}a", f"목표{week_number}b"]
            )
        )
        return await SummaryRepositoryImpl(test_session).save(
            Summary(
                user_id=test_data.test_user.id,
                week_topic_id=new_week_topic.id,
                content=f"테스트 요약본 {week_number}",
                is_public=True
            )
        )

    @pytest.mark.asyncio
    async def test_save_and_find_by_id(self, test_session, repository, test_data):
        feedback = Feedback(
            summary_id=test_data.test_summary.id,
            content="피드백 내용"
        )
        saved_feedback = await repository.save(feedback)
        found_feedback = await repository.find_by_id(feedback_id=saved_feedback.id)
        assert found_feedback is not None
        assert found_feedback.summary_id == test_data.test_summary.id
        assert found_feedback.content == "피드백 내용"

    @pytest.mark.asyncio
    async def test_save_and_find_by_summary_id(self, test_session, repository, test_data):
        feedback = Feedback(
            summary_id=test_data.test_summary.id,
            content="피드백 내용"
        )
        await repository.save(feedback)
        found_feedback = await repository.find_by_summary_id(summary_id=test_data.test_summary.id)
        assert found_feedback is not None
        assert found_feedback.content == "피드백 내용"

    @pytest.mark.asyncio
    async def test_save_and_find_all(self, test_session, repository, test_data):
        feedback1 = Feedback(
            summary_id=test_data.test_summary.id,
            content="피드백 내용"
        )
        await repository.save(feedback1)
        week2_summary = await self.create_additional_summary_by_week(test_session=test_session,
                                                             test_data=test_data,
                                                             week_number=2)
        feedback2 = Feedback(
            summary_id=week2_summary.id,
            content="피드백2 내용"
        )
        await repository.save(feedback2)
        found_feedbacks: List[Feedback] = await repository.find_all()
        assert len(found_feedbacks) == 2
        found_feedback_1, found_feedback_2 = found_feedbacks
        assert found_feedback_1.summary_id == test_data.test_summary.id
        assert found_feedback_1.content == "피드백 내용"
        assert found_feedback_2.summary_id == week2_summary.id
        assert found_feedback_2.content == "피드백2 내용"

    @pytest.mark.asyncio
    async def test_domain_entity_conversion(self, test_session, repository, test_data):
        original_feedback = Feedback(
            summary_id=test_data.test_summary.id,
            content="피드백 내용"
        )
        await repository.save(original_feedback)
        found_feedback = await repository.find_by_summary_id(summary_id=test_data.test_summary.id)
        assert isinstance(found_feedback, Feedback)
        assert found_feedback.summary_id == test_data.test_summary.id
        assert found_feedback.content == "피드백 내용"