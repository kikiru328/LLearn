from dataclasses import dataclass
from datetime import datetime
from typing import List
from uuid import UUID


@dataclass
class GenerateFeedbackUseCaseRequest:
    """GenerateFeedbackUseCase 입력 DTO"""
    summary_id: UUID


@dataclass
class GenerateFeedbackUseCaseResponse:
    """GenerateFeedbackUseCase 출력 DTO"""
    id: UUID
    summary_id: UUID
    content: str  # 5단계 구조화된 피드백
    created_at: datetime
    
@dataclass
class GetFeedbackRequest:
    """피드백 조회 요청"""
    summary_id: UUID
    user_id: UUID  # 권한 확인용

@dataclass
class GetFeedbackResponse:
    """피드백 조회 응답"""
    id: UUID
    summary_id: UUID
    content: str  # 5단계 피드백 전체 내용
    created_at: datetime
    
    # 연관 정보
    summary_content: str  # 어떤 요약에 대한 피드백인지
    week_topic_title: str  # 어떤 주차인지
    

@dataclass
class GetUserFeedbacksRequest:
    """사용자 피드백 목록 조회 요청"""
    user_id: UUID

@dataclass
class FeedbackSummaryData:
    """피드백 목록용 데이터"""
    id: UUID
    summary_id: UUID
    week_topic_title: str
    curriculum_title: str
    content_preview: str  # 피드백 앞 100자
    created_at: datetime

@dataclass
class GetUserFeedbacksResponse:
    """사용자 피드백 목록 조회 응답"""
    feedbacks: List[FeedbackSummaryData]