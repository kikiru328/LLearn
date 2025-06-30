from domain.entities.summary import Summary
from domain.repositories.summary_repository import SummaryRepository
from domain.repositories.week_topic_repository import WeekTopicRepository
from usecase.dto.summary_dto import CreateSummaryUseCaseRequest, CreateSummaryUseCaseResponse


class CreateSummaryUseCase:
    def __init__(
        self,
        summary_repository: SummaryRepository,
        week_topic_repository: WeekTopicRepository
    ):
        self.summary_repository = summary_repository
        self.week_topic_repository = week_topic_repository
        
    async def execute(self, request: CreateSummaryUseCaseRequest) -> CreateSummaryUseCaseResponse:
        week_topic = await self.week_topic_repository.find_by_id(request.week_topic_id)
        if not week_topic:
            raise ValueError("존재하지 않는 주차 주제입니다")
        
        summary = Summary(
            user_id=request.user_id,
            week_topic_id=request.week_topic_id,
            content=request.content,
            is_public=request.is_public
        )
        
        saved_summary = await self.summary_repository.save(summary)
        
        return CreateSummaryUseCaseResponse(
            id=saved_summary.id,
            user_id=saved_summary.user_id,
            week_topic_id=saved_summary.week_topic_id,
            content=saved_summary.content,
            is_public=saved_summary.is_public,
            created_at=saved_summary.created_at,
            updated_at=saved_summary.updated_at
        )