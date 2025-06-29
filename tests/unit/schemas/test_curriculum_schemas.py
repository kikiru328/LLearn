import pytest
from pydantic import ValidationError
from uuid import uuid4
from datetime import datetime, timezone

from app.schemas.curriculum import GenerateCurriculumRequest, SaveCurriculumRequest, CurriculumSummary, \
    CurriculumResponse, ListCurriculumResponse
from app.schemas.week_topic import WeekTopicData, WeekTopicResponse


class TestGenerateCurriculumRequest:
    def test_valid_generate_request(self):
        """정상적 generate curriculum"""
        data = GenerateCurriculumRequest(
            goal="Python 기초",
            duration_weeks=4
        )
        assert data.goal=="Python 기초"
        assert data.duration_weeks==4
        
    
    def test_default_duration_request(self):
        data = GenerateCurriculumRequest(
            goal="JavaScript 기초"
        )
        assert data.duration_weeks==12
        
    def test_invalid_goal_too_short(self):
        with pytest.raises(ValidationError):
            GenerateCurriculumRequest(
                goal="짧"
            )
            
    def test_invalid_goal_too_ling(self):
        with pytest.raises(ValidationError):
            GenerateCurriculumRequest(
                goal="시도"*200
            )
    
    def test_invalid_duration_weeks_too_large(self):
        with pytest.raises(ValidationError):
            GenerateCurriculumRequest(
                goal="Python 기초",
                duration_weeks=27
            )

class TestSaveCurriculumRequest:
    def test_valid_save_request(self):
        week_data = WeekTopicData(
            week_number=1,
            title="1주차 Python 기초",
            description="파이썬 기초",
            learning_goals=["변수", "함수"]
        )
        
        request = SaveCurriculumRequest(
            goal="Python 마스터",
            duration_weeks=12,
            title="Python 마스터되기",
            weeks=[week_data],
            is_public=True
        )
        assert len(request.weeks)==1
        assert request.is_public==True

    def test_invalid_title_too_long(self):
        week_data = WeekTopicData(
            week_number=1,
            title="1주차 Python 기초",
            description="파이썬 기초",
            learning_goals=["변수", "함수"]
        )

        with pytest.raises(ValidationError):
            SaveCurriculumRequest(
                goal="파이썬",
                duration_weeks=12,
                title="Python 마스터되기"*300,
                weeks=[week_data],
                is_public=True
            )

    def test_empty_week_list(self):
        with pytest.raises(ValidationError):
            SaveCurriculumRequest(
                goal="파이썬",
                duration_weeks=12,
                title="Python 마스터되기",
                weeks=[],
                is_public=True
            )

class TestCurriculumSummary:
    def test_valid_curriculum_summary(self):
        curriculum_id = uuid4()
        now = datetime.now(timezone.utc)

        summary = CurriculumSummary(
            id=curriculum_id,
            title="파이썬 마스터하기",
            goal="Python Master",
            duration_weeks=12,
            is_public=True,
            created_at=now,
            updated_at=now
        )

        assert summary.id==curriculum_id
        assert summary.title == "파이썬 마스터하기"
        assert summary.goal == "Python Master"
        assert summary.duration_weeks == 12
        assert summary.is_public is True
        assert summary.created_at == now

    def test_curriculum_summary_from_dict(self):
        data = {
            "id": str(uuid4()),
            "title": "JavaScript 기초",
            "goal": "JS 마스터하기",
            "duration_weeks": 8,
            "is_public": False,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }

        summary = CurriculumSummary(**data)
        assert summary.title == "JavaScript 기초"
        assert summary.duration_weeks == 8
        assert summary.is_public is False

class TestCurriculumResponse:
    def test_with_weeks(self):
        curriculum_id = uuid4()
        user_id = uuid4()
        now = datetime.now(timezone.utc)


        week_response = WeekTopicResponse(
            id=uuid4(),
            curriculum_id=uuid4(),
            week_number=1,
            title="1주차 파이썬 기초",
            description= "파이썬 강좌",
            learning_goals= ["변수", "함수"],
            created_at=now,
            updated_at=now
        )

        curriculum_response = CurriculumResponse(
            id=curriculum_id,
            user_id=user_id,
            goal="Python 마스터하기",
            title="12주 Python 완전정복",
            duration_weeks=12,
            is_public=True,
            created_at=now,
            updated_at=now,
            weeks=[week_response]  # 주차 정보 포함
        )

        assert curriculum_response.id == curriculum_id
        assert curriculum_response.user_id == user_id
        assert len(curriculum_response.weeks) == 1
        assert curriculum_response.weeks[0].week_number == 1
        assert curriculum_response.weeks[0].title == "1주차 파이썬 기초"

class TestListCurriculumResponse:
    def test_valid_curriculums(self):
        now = datetime.now(timezone.utc)

        summary_1 = CurriculumSummary(
            id=uuid4(),
            title="파이썬 마스터하기",
            goal="Python Master",
            duration_weeks=12,
            is_public=True,
            created_at=now,
            updated_at=now
        )
        summary_2 = CurriculumSummary(
            id=uuid4(),
            title="자바스크립트 마스터하기",
            goal="JS Master",
            duration_weeks=12,
            is_public=True,
            created_at=now,
            updated_at=now
        )
        curriculums = [summary_1,summary_2]
        list_curriculum_response = ListCurriculumResponse(
            curriculums=curriculums,
            total=len(curriculums),
            page=1,
            size=2,
            has_next=False
        )
        assert list_curriculum_response.total == 2
        assert list_curriculum_response.page == 1
        assert list_curriculum_response.size == 2
        assert list_curriculum_response.has_next is False
        assert list_curriculum_response.curriculums[0].title == "파이썬 마스터하기"
        assert list_curriculum_response.curriculums[1].title == "자바스크립트 마스터하기"