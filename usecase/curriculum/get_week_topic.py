from domain.repositories.curriculum_repository import CurriculumRepository
from domain.repositories.week_topic_repository import WeekTopicRepository
from usecase.dto.curriculum_dto import GetWeekTopicRequest, GetWeekTopicResponse

class GetWeekTopicUseCase:
    def __init__(
        self,
        curriculum_repository: CurriculumRepository,
        week_topic_repository: WeekTopicRepository
    ):
        self.curriculum_repository = curriculum_repository
        self.week_topic_repository = week_topic_repository
    
    async def execute(self, request: GetWeekTopicRequest) -> GetWeekTopicResponse:

        curriculum = await self.curriculum_repository.find_by_id(request.curriculum_id)
        if not curriculum:
            raise ValueError("커리큘럼을 찾을 수 없습니다")
        
        if curriculum.user_id != request.user_id and not curriculum.is_public:
            raise ValueError("접근 권한이 없습니다")

        week_topic = await self.week_topic_repository.find_by_curriculum_and_week(
            request.curriculum_id, 
            request.week_number
        )
        if not week_topic:
            raise ValueError(f"{request.week_number}주차를 찾을 수 없습니다")

        return GetWeekTopicResponse(
            id=week_topic.id,
            curriculum_id=week_topic.curriculum_id,
            week_number=week_topic.week_number,
            title=week_topic.title,
            description=week_topic.description,
            learning_goals=week_topic.learning_goals,
            curriculum_title=curriculum.title,  # 커리큘럼 제목 추가
            created_at=week_topic.created_at,
            updated_at=week_topic.updated_at
        )