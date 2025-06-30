from domain.entities.feedback import Feedback
from domain.repositories.feedback_repository import FeedbackRepository
from domain.repositories.summary_repository import SummaryRepository
from domain.repositories.week_topic_repository import WeekTopicRepository
from domain.services.llm_service import LLMService
from usecase.dto.feedback_dto import GenerateFeedbackUseCaseRequest, GenerateFeedbackUseCaseResponse


class GenerateFeedbackUseCase:
    def __init__(
        self,
        feedback_repository: FeedbackRepository,
        summary_repository: SummaryRepository,
        week_topic_repository: WeekTopicRepository,
        llm_service: LLMService
    ):
        self.feedback_repository = feedback_repository
        self.summary_repository = summary_repository
        self.week_topic_repository = week_topic_repository
        self.llm_service = llm_service
        
    async def execute(self, request: GenerateFeedbackUseCaseRequest) -> GenerateFeedbackUseCaseResponse:
        summary = await self.summary_repository.find_by_id(request.summary_id)
        if not summary:
            raise ValueError("존재하지 않는 요약입니다")
        
        week_topic = await self.week_topic_repository.find_by_id(summary.week_topic_id)
        if not week_topic:
            raise ValueError("연관된 주차 주제를 찾을 수 없습니다")

        feedback_content = await self.llm_service.generate_feedback(
            summary_content=summary.content,
            week_topic_title=week_topic.title,
            week_topic_description=week_topic.description,
            learning_goals=week_topic.learning_goals
        )
        
        feedback = Feedback(
            summary_id=request.summary_id,
            content=feedback_content
        )
        
        saved_feedback = await self.feedback_repository.save(feedback)
        
        return GenerateFeedbackUseCaseResponse(
            id=saved_feedback.id,
            summary_id=saved_feedback.summary_id,
            content=saved_feedback.content,
            created_at=saved_feedback.created_at
        )