from domain.repositories.summary_repository import SummaryRepository
from domain.repositories.week_topic_repository import WeekTopicRepository
from domain.repositories.curriculum_repository import CurriculumRepository
from usecase.dto.summary_dto import GetSummaryDetailRequest, GetSummaryDetailResponse

class GetSummaryDetailUseCase:
    def __init__(
        self,
        summary_repository: SummaryRepository,
        week_topic_repository: WeekTopicRepository,
        curriculum_repository: CurriculumRepository
    ):
        self.summary_repository = summary_repository
        self.week_topic_repository = week_topic_repository
        self.curriculum_repository = curriculum_repository
    
    async def execute(self, request: GetSummaryDetailRequest) -> GetSummaryDetailResponse:
        # 1. 요약 조회
        summary = await self.summary_repository.find_by_id(request.summary_id)
        if not summary:
            raise ValueError("요약을 찾을 수 없습니다")
        
        # 2. 권한 확인 (본인 요약 또는 공개 요약)
        if summary.user_id != request.user_id and not summary.is_public:
            raise ValueError("접근 권한이 없습니다")
        
        # 3. 주차 정보 조회
        week_topic = await self.week_topic_repository.find_by_id(summary.week_topic_id)
        if not week_topic:
            raise ValueError("연관된 주차 정보를 찾을 수 없습니다")
        
        # 4. 커리큘럼 정보 조회
        curriculum = await self.curriculum_repository.find_by_id(week_topic.curriculum_id)
        if not curriculum:
            raise ValueError("연관된 커리큘럼 정보를 찾을 수 없습니다")
        
        # 5. 응답 생성
        return GetSummaryDetailResponse(
            id=summary.id,
            user_id=summary.user_id,
            week_topic_id=summary.week_topic_id,
            content=summary.content,  # 전체 내용
            is_public=summary.is_public,
            created_at=summary.created_at,
            updated_at=summary.updated_at,
            
            # 연관 정보들
            week_topic_title=week_topic.title,
            week_topic_description=week_topic.description,
            learning_goals=week_topic.learning_goals,
            curriculum_title=curriculum.title,
            curriculum_goal=curriculum.goal
        )