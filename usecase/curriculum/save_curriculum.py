from domain.entities.curriculum import Curriculum
from domain.entities.week_topic import WeekTopic
from domain.repositories.curriculum_repository import CurriculumRepository
from domain.repositories.week_topic_repository import WeekTopicRepository
from usecase.dto.curriculum_dto import SaveCurriculumUseCaseRequest, SaveCurriculumUseCaseResponse, WeekTopicData


class SaveCurriculumUseCase:
    def __init__(
        self,
        curriculum_repository: CurriculumRepository,
        week_topic_repository: WeekTopicRepository
    ):
        self.curriculum_repository = curriculum_repository
        self.week_topic_repository = week_topic_repository
        
    async def execute(self, request: SaveCurriculumUseCaseRequest) -> SaveCurriculumUseCaseResponse:
        curriculum = Curriculum(
            user_id=request.user_id,
            title=request.title,
            goal=request.goal,
            duration_weeks=len(request.weeks),
            is_public=request.is_public
        )
        
        saved_curriculum = await self.curriculum_repository.save(curriculum)
        
        saved_weeks = []
        for week_data in request.weeks:
            week_topic = WeekTopic(
                curriculum_id=saved_curriculum.id,
                week_number=week_data.week_number,
                title=week_data.title,
                description=week_data.description,
                learning_goals=week_data.learning_goals
            )
            saved_week = await self.week_topic_repository.save(week_topic)
            saved_weeks.append(saved_week)
        
        return SaveCurriculumUseCaseResponse(
            id=saved_curriculum.id,
            user_id=saved_curriculum.user_id,
            title=saved_curriculum.title,
            goal=saved_curriculum.goal,
            duration_weeks=saved_curriculum.duration_weeks,
            weeks=[
                WeekTopicData(
                    week_number=week.week_number,
                    title=week.title,
                    description=week.description,
                    learning_goals=week.learning_goals
                )
                for week in saved_weeks
            ],
            is_public=saved_curriculum.is_public,
            created_at=saved_curriculum.created_at,
            updated_at=saved_curriculum.updated_at
        )