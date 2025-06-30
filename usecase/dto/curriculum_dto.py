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
class GeneratePreviewRequest:
    """커리큘럼 미리보기 생성 요청"""
    goal: str
    duration_weeks: int
    
    def __post_init__(self):
        if not self.goal or len(self.goal.strip()) < 50:
            raise ValueError("학습 목표는 50자 이상이어야 합니다")
        if len(self.goal.strip()) > 200:
            raise ValueError("학습 목표는 200자 이하여야 합니다")
        if self.duration_weeks < 1 or self.duration_weeks > 26:
            raise ValueError("학습 기간은 1-26주 사이여야 합니다")
        
        # 공백 제거
        self.goal = self.goal.strip()


@dataclass
class GeneratePreviewResponse:
    """커리큘럼 미리보기 생성 응답"""
    title: str  # LLM이 생성한 커리큘럼 제목
    goal: str
    duration_weeks: int
    weeks: List[WeekTopicData]  # LLM이 생성 (desc

@dataclass
class SaveCurriculumUseCaseRequest:
    """SaveCurriculumUseCase 입력 DTO"""
    user_id: UUID
    title: str
    goal: str
    weeks: List[WeekTopicData]
    is_public: bool = False


@dataclass
class SaveCurriculumUseCaseResponse:
    """SaveCurriculumUseCase 출력 DTO"""
    id: UUID
    user_id: UUID
    title: str
    goal: str
    duration_weeks: int
    weeks: List[WeekTopicData]
    is_public: bool
    created_at: datetime
    updated_at: datetime
    
    
@dataclass
class GetUserCurriculumsRequest:
    """사용자 커리큘럼 목록 조회 요청"""
    user_id: UUID

@dataclass  
class CurriculumSummaryData:
    """커리큘럼 요약 정보 (목록용)"""
    id: UUID
    title: str
    goal: str
    duration_weeks: int
    is_public: bool
    created_at: datetime
    updated_at: datetime

@dataclass
class GetUserCurriculumsResponse:
    """사용자 커리큘럼 목록 조회 응답"""
    curriculums: List[CurriculumSummaryData]
    
@dataclass
class GetCurriculumDetailRequest:
    """커리큘럼 상세 조회 요청"""
    curriculum_id: UUID
    user_id: UUID  # 권한 확인용 (본인 커리큘럼인지)

@dataclass
class GetCurriculumDetailResponse:
    """커리큘럼 상세 조회 응답"""
    id: UUID
    user_id: UUID
    title: str
    goal: str
    duration_weeks: int
    weeks: List[WeekTopicData]  # 전체 주차별 상세 정보
    is_public: bool
    created_at: datetime
    updated_at: datetime
    

@dataclass
class GetWeekTopicRequest:
    """주차별 상세 조회 요청"""
    curriculum_id: UUID
    week_number: int
    user_id: UUID  # 권한 확인용

@dataclass
class GetWeekTopicResponse:
    """주차별 상세 조회 응답"""
    id: UUID
    curriculum_id: UUID
    week_number: int
    title: str
    description: str
    learning_goals: List[str]
    curriculum_title: str  # 어떤 커리큘럼인지 표시용
    created_at: datetime
    updated_at: datetime