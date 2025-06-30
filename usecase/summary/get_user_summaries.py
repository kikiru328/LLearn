from domain.repositories.summary_repository import SummaryRepository
from domain.repositories.week_topic_repository import WeekTopicRepository
from domain.repositories.curriculum_repository import CurriculumRepository
from usecase.dto.summary_dto import GetUserSummariesRequest, GetUserSummariesResponse, SummarySummaryData

class GetUserSummariesUseCase:
    def __init__(
        self,
        summary_repository: SummaryRepository,
        week_topic_repository: WeekTopicRepository,
        curriculum_repository: CurriculumRepository
    ):
        self.summary_repository = summary_repository
        self.week_topic_repository = week_topic_repository
        self.curriculum_repository = curriculum_repository
    
    async def execute(self, request: GetUserSummariesRequest) -> GetUserSummariesResponse:
        # 1. 사용자의 모든 요약 조회
        summaries = await self.summary_repository.find_by_user_id(request.user_id)
        
        # 2. 각 요약에 대해 주차 및 커리큘럼 정보 조회
        summary_data_list = []
        for summary in summaries:
            # 주차 정보 조회
            week_topic = await self.week_topic_repository.find_by_id(summary.week_topic_id)
            if not week_topic:
                continue  # 주차 정보가 없으면 스킵
            
            # 커리큘럼 정보 조회
            curriculum = await self.curriculum_repository.find_by_id(week_topic.curriculum_id)
            if not curriculum:
                continue  # 커리큘럼 정보가 없으면 스킵
            
            # 내용 미리보기 생성 (앞 100자)
            content_preview = summary.content[:100] + "..." if len(summary.content) > 100 else summary.content
            
            summary_data = SummarySummaryData(
                id=summary.id,
                week_topic_title=week_topic.title,
                curriculum_title=curriculum.title,
                content_preview=content_preview,
                created_at=summary.created_at,
                updated_at=summary.updated_at
            )
            summary_data_list.append(summary_data)
        
        # 3. 최신순으로 정렬
        summary_data_list.sort(key=lambda x: x.created_at, reverse=True)
        
        return GetUserSummariesResponse(summaries=summary_data_list)