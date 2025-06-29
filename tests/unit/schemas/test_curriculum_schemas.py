import pytest
from pydantic import ValidationError
from uuid import uuid4
from datetime import datetime

from app.schemas.curriculum import GenerateCurriculumRequest, SaveCurriculumRequest
from app.schemas.week_topic import WeekTopicData

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