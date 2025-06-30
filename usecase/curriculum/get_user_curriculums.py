from domain.repositories.curriculum_repository import CurriculumRepository
from usecase.dto.curriculum_dto import GetUserCurriculumsRequest, GetUserCurriculumsResponse, CurriculumSummaryData

class GetUserCurriculumsUseCase:
    def __init__(self, curriculum_repository: CurriculumRepository):
        self.curriculum_repository = curriculum_repository
    
    async def execute(self, request: GetUserCurriculumsRequest) -> GetUserCurriculumsResponse:
        curriculums = await self.curriculum_repository.find_by_user_id(request.user_id)
        
        curriculum_summaries = [
            CurriculumSummaryData(
                id=curriculum.id,
                title=curriculum.title,
                goal=curriculum.goal,
                duration_weeks=curriculum.duration_weeks,
                is_public=curriculum.is_public,
                created_at=curriculum.created_at,
                updated_at=curriculum.updated_at
            )
            for curriculum in curriculums
        ]
        
        return GetUserCurriculumsResponse(curriculums=curriculum_summaries)