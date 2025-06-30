from dataclasses import dataclass
from datetime import datetime
from typing import List
from uuid import UUID


@dataclass
class CreateSummaryUseCaseRequest:
    """CreateSummaryUseCase 입력 DTO"""
    user_id: UUID
    week_topic_id: UUID
    content: str
    is_public: bool = False


@dataclass
class CreateSummaryUseCaseResponse:
    """CreateSummaryUseCase 출력 DTO"""
    id: UUID
    user_id: UUID
    week_topic_id: UUID
    content: str
    is_public: bool
    created_at: datetime
    updated_at: datetime
    
@dataclass
class GetUserSummariesRequest:
    """사용자 요약 목록 조회 요청"""
    user_id: UUID

@dataclass
class SummarySummaryData:
    """요약 목록용 데이터 (간단한 정보만)"""
    id: UUID
    week_topic_title: str      # "1주차: 컴퓨터구조 기초"
    curriculum_title: str      # "CS 기초 과정"
    content_preview: str       # 내용 앞 100자 미리보기
    created_at: datetime
    updated_at: datetime

@dataclass
class GetUserSummariesResponse:
    """사용자 요약 목록 조회 응답"""
    summaries: List[SummarySummaryData]
    
    
@dataclass
class GetSummaryDetailRequest:
    """요약 상세 조회 요청"""
    summary_id: UUID
    user_id: UUID  # 권한 확인용 (본인 요약 또는 공개 요약)

@dataclass
class GetSummaryDetailResponse:
    """요약 상세 조회 응답"""
    id: UUID
    user_id: UUID
    week_topic_id: UUID
    content: str  # 전체 내용
    is_public: bool
    created_at: datetime
    updated_at: datetime
    
    # 연관 정보들
    week_topic_title: str
    week_topic_description: str
    learning_goals: List[str]
    curriculum_title: str
    curriculum_goal: str
    
@dataclass
class GetWeekSummariesRequest:
    """특정 주차의 요약 목록 조회 요청"""
    week_topic_id: UUID
    user_id: UUID  # 권한 확인용 (해당 주차에 접근 가능한지)

@dataclass
class WeekSummaryData:
    """주차별 요약 목록용 데이터"""
    id: UUID
    user_id: UUID  # 작성자 (익명화 가능)
    content_preview: str  # 앞 150자 미리보기
    created_at: datetime
    # 작성자 정보는 나중에 추가 가능 (nickname 등)

@dataclass
class GetWeekSummariesResponse:
    """특정 주차의 요약 목록 조회 응답"""
    week_topic_title: str     # "1주차: 컴퓨터구조 기초"
    curriculum_title: str     # "CS 기초 과정"
    summaries: List[WeekSummaryData]