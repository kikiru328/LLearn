from domain.repositories.feedback_repository import FeedbackRepository
from domain.repositories.summary_repository import SummaryRepository
from domain.repositories.week_topic_repository import WeekTopicRepository
from usecase.dto.feedback_dto import GetFeedbackRequest, GetFeedbackResponse

class GetFeedbackUseCase:
    def __init__(
        self,
        feedback_repository: FeedbackRepository,
        summary_repository: SummaryRepository,
        week_topic_repository: WeekTopicRepository
    ):
        self.feedback_repository = feedback_repository
        self.summary_repository = summary_repository
        self.week_topic_repository = week_topic_repository
    
    async def execute(self, request: GetFeedbackRequest) -> GetFeedbackResponse:
        # 1. 요약 조회 및 권한 확인
        summary = await self.summary_repository.find_by_id(request.summary_id)
        if not summary:
            raise ValueError("요약을 찾을 수 없습니다")
        
        if summary.user_id != request.user_id and not summary.is_public:
            raise ValueError("접근 권한이 없습니다")
        
        # 2. 피드백 조회
        feedback = await self.feedback_repository.find_by_summary_id(request.summary_id)
        if not feedback:
            raise ValueError("피드백을 찾을 수 없습니다")
        
        # 3. 주차 정보 조회 (제목용)
        week_topic = await self.week_topic_repository.find_by_id(summary.week_topic_id)
        week_topic_title = week_topic.title if week_topic else "알 수 없는 주차"
        
        # 4. 응답 생성
        return GetFeedbackResponse(
            id=feedback.id,
            summary_id=feedback.summary_id,
            content=feedback.content,
            created_at=feedback.created_at,
            summary_content=summary.content,
            week_topic_title=week_topic_title
        )