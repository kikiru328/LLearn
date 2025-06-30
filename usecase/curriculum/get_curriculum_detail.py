from domain.repositories.curriculum_repository import CurriculumRepository
from domain.repositories.week_topic_repository import WeekTopicRepository
from usecase.dto.curriculum_dto import GetCurriculumDetailRequest, GetCurriculumDetailResponse, WeekTopicData

class GetCurriculumDetailUseCase:
    def __init__(
        self,
        curriculum_repository: CurriculumRepository,
        week_topic_repository: WeekTopicRepository
    ):
        self.curriculum_repository = curriculum_repository
        self.week_topic_repository = week_topic_repository
    
    async def execute(self, request: GetCurriculumDetailRequest) -> GetCurriculumDetailResponse:

        curriculum = await self.curriculum_repository.find_by_id(request.curriculum_id)
        if not curriculum:
            raise ValueError("커리큘럼을 찾을 수 없습니다")
        
        if curriculum.user_id != request.user_id and not curriculum.is_public:
            raise ValueError("접근 권한이 없습니다")

        week_topics = await self.week_topic_repository.find_by_curriculum_id(request.curriculum_id)
        
        week_data_list = [
            WeekTopicData(
                week_number=topic.week_number,
                title=topic.title,
                description=topic.description,
                learning_goals=topic.learning_goals
            )
            for topic in sorted(week_topics, key=lambda x: x.week_number)  # 주차 순서대로 정렬
        ]

        return GetCurriculumDetailResponse(
            id=curriculum.id,
            user_id=curriculum.user_id,
            title=curriculum.title,
            goal=curriculum.goal,
            duration_weeks=curriculum.duration_weeks,
            weeks=week_data_list,
            is_public=curriculum.is_public,
            created_at=curriculum.created_at,
            updated_at=curriculum.updated_at
        )