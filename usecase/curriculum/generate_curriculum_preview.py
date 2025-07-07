from domain.services.llm_service import LLMService
from usecase.dto.curriculum_dto import GeneratePreviewRequest, GeneratePreviewResponse, WeekTopicData

class GenerateCurriculumPreviewUseCase:
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service
    
    async def execute(self, request: GeneratePreviewRequest) -> GeneratePreviewResponse:

        llm_response = await self.llm_service.generate_curriculum(
            goal=request.goal,
            duration_weeks=request.duration_weeks
        )
        
        weeks = [
            WeekTopicData(
                week_number=week["week_number"],
                title=week["title"], 
                description="",  # 사용자가 나중에 입력
                learning_goals=week["learning_goals"]
            )
            for week in llm_response["weeks"]
        ]
        
        return GeneratePreviewResponse(
            title=llm_response["title"],
            goal=request.goal,
            duration_weeks=request.duration_weeks,
            weeks=weeks
        )