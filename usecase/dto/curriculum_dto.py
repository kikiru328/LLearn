from dataclasses import dataclass
from datetime import datetime
from typing import List
from uuid import UUID


@dataclass  
class WeekTopicData:
    """주차별 주제 데이터"""
    week_number: int
    title: str
    description: str
    learning_goals: List[str]


@dataclass
class CreateCurriculumUseCaseRequest:
    """CreateCurriculumUseCase 입력 DTO"""
    user_id: UUID
    title: str
    goal: str
    weeks: List[WeekTopicData]
    is_public: bool = False


@dataclass
class CreateCurriculumUseCaseResponse:
    """CreateCurriculumUseCase 출력 DTO"""
    id: UUID
    user_id: UUID
    title: str
    goal: str
    duration_weeks: int
    weeks: List[WeekTopicData]
    is_public: bool
    created_at: datetime
    updated_at: datetime