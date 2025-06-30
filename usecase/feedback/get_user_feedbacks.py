from domain.repositories.feedback_repository import FeedbackRepository
from domain.repositories.summary_repository import SummaryRepository
from domain.repositories.week_topic_repository import WeekTopicRepository
from domain.repositories.curriculum_repository import CurriculumRepository
from usecase.dto.feedback_dto import GetUserFeedbacksRequest, GetUserFeedbacksResponse, FeedbackSummaryData

class GetUserFeedbacksUseCase:
    def __init__(
        self,
        feedback_repository: FeedbackRepository,
        summary_repository: SummaryRepository,
        week_topic_repository: WeekTopicRepository,
        curriculum_repository: CurriculumRepository
    ):
        self.feedback_repository = feedback_repository
        self.summary_repository = summary_repository
        self.week_topic_repository = week_topic_repository
        self.curriculum_repository = curriculum_repository
    
    async def execute(self, request: GetUserFeedbacksRequest) -> GetUserFeedbacksResponse:
        # 1. 사용자의 모든 요약 조회
        summaries = await self.summary_repository.find_by_user_id(request.user_id)
        
        # 2. 각 요약의 피드백 조회
        feedback_data_list = []
        for summary in summaries:
            feedback = await self.feedback_repository.find_by_summary_id(summary.id)
            if not feedback:
                continue
            
            # 주차 및 커리큘럼 정보
            week_topic = await self.week_topic_repository.find_by_id(summary.week_topic_id)
            if not week_topic:
                continue
            
            curriculum = await self.curriculum_repository.find_by_id(week_topic.curriculum_id)
            if not curriculum:
                continue
            
            # 피드백 미리보기
            content_preview = feedback.content[:100] + "..." if len(feedback.content) > 100 else feedback.content
            
            feedback_data = FeedbackSummaryData(
                id=feedback.id,
                summary_id=feedback.summary_id,
                week_topic_title=week_topic.title,
                curriculum_title=curriculum.title,
                content_preview=content_preview,
                created_at=feedback.created_at
            )
            feedback_data_list.append(feedback_data)
        
        # 3. 최신순 정렬
        feedback_data_list.sort(key=lambda x: x.created_at, reverse=True)
        
        return GetUserFeedbacksResponse(feedbacks=feedback_data_list)