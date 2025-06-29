import pytest
from pydantic import ValidationError
from uuid import uuid4
from datetime import datetime
from typing import Optional
from app.schemas.week_topic import (
    WeekTopicData,
    WeekTopicResponse,
    UpdateWeekTopicRequest,
)


class TestWeekTopicData:
    def test_valid_week_topic_data(self):
        """정상적인 WeekTopicData 테스트"""
        data = WeekTopicData(
            week_number=1,
            title="1주차 Python 기초",
            description="파이썬의 기본 개념을 학습합니다",
            learning_goals=["변수와 자료형", "조건문", "반복문"]
        )
        assert data.week_number == 1
        assert data.title == "1주차 Python 기초"
        assert len(data.learning_goals) == 3

    def test_invalid_week_number_zero(self):
        """week_number가 0일 때 에러 테스트"""
        with pytest.raises(ValidationError):
            WeekTopicData(
                week_number=0,
                title="테스트",
                description="설명",
                learning_goals=["목표1"]
            )

    def test_invalid_week_number_negative(self):
        """week_number가 음수일 때 에러 테스트"""
        with pytest.raises(ValidationError):
            WeekTopicData(
                week_number=-1,
                title="테스트",
                description="설명",
                learning_goals=["목표1"]
            )

    def test_invalid_title_empty(self):
        """title이 빈 문자열일 때 에러 테스트"""
        with pytest.raises(ValidationError):
            WeekTopicData(
                week_number=1,
                title="",
                description="설명",
                learning_goals=["목표1"]
            )

    def test_invalid_title_too_long(self):
        """title이 너무 길 때 에러 테스트"""
        with pytest.raises(ValidationError):
            WeekTopicData(
                week_number=1,
                title="a" * 101,  # 100자 초과
                description="설명",
                learning_goals=["목표1"]
            )

    def test_invalid_learning_goals_empty(self):
        """learning_goals가 빈 리스트일 때 에러 테스트"""
        with pytest.raises(ValidationError):
            WeekTopicData(
                week_number=1,
                title="테스트",
                description="설명",
                learning_goals=[]
            )

    def test_valid_description_empty(self):
        """description은 빈 문자열도 허용"""
        data = WeekTopicData(
            week_number=1,
            title="테스트",
            description="",  # 빈 문자열 허용
            learning_goals=["목표1"]
        )
        assert data.description == ""


class TestWeekTopicResponse:
    def test_valid_week_topic_response(self):
        """정상적인 WeekTopicResponse 테스트"""
        week_id = uuid4()
        curriculum_id = uuid4()
        now = datetime.now()
        
        response = WeekTopicResponse(
            id=week_id,
            curriculum_id=curriculum_id,
            week_number=1,
            title="1주차 Python 기초",
            description="파이썬 기초를 학습합니다",
            learning_goals=["변수", "함수"],
            created_at=now,
            updated_at=now
        )
        
        assert response.id == week_id
        assert response.curriculum_id == curriculum_id
        assert response.week_number == 1
        assert len(response.learning_goals) == 2

    def test_week_topic_response_from_dict(self):
        """딕셔너리로부터 WeekTopicResponse 생성 테스트"""
        data = {
            "id": str(uuid4()),
            "curriculum_id": str(uuid4()),
            "week_number": 2,
            "title": "2주차 제목",
            "description": "2주차 설명",
            "learning_goals": ["목표1", "목표2", "목표3"],
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        response = WeekTopicResponse(**data)
        assert response.week_number == 2
        assert response.title == "2주차 제목"
        assert len(response.learning_goals) == 3


class TestUpdateWeekTopicRequest:
    def test_valid_update_request_all_fields(self):
        """모든 필드를 포함한 수정 요청 테스트"""
        request = UpdateWeekTopicRequest(
            title="수정된 제목",
            description="수정된 설명",
            learning_goals=["수정된 목표1", "수정된 목표2"]
        )
        assert request.title == "수정된 제목"
        assert request.description == "수정된 설명"
        assert len(request.learning_goals) == 2

    def test_valid_update_request_partial(self):
        """부분 필드만 포함한 수정 요청 테스트"""
        request = UpdateWeekTopicRequest(title="제목만 수정")
        assert request.title == "제목만 수정"
        assert request.description is None
        assert request.learning_goals is None

    def test_valid_update_request_empty(self):
        """빈 수정 요청 테스트 (모든 필드 Optional)"""
        request = UpdateWeekTopicRequest()
        assert request.title is None
        assert request.description is None
        assert request.learning_goals is None

    def test_invalid_update_title_empty(self):
        """빈 title로 수정 시 에러 테스트"""
        with pytest.raises(ValidationError):
            UpdateWeekTopicRequest(title="")

    def test_invalid_update_title_too_long(self):
        """너무 긴 title로 수정 시 에러 테스트"""
        with pytest.raises(ValidationError):
            UpdateWeekTopicRequest(title="a" * 101)

    def test_invalid_update_learning_goals_empty(self):
        """빈 learning_goals로 수정 시 에러 테스트"""
        with pytest.raises(ValidationError):
            UpdateWeekTopicRequest(learning_goals=[])