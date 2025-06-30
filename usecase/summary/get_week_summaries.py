from domain.repositories.summary_repository import SummaryRepository
from domain.repositories.week_topic_repository import WeekTopicRepository
from domain.repositories.curriculum_repository import CurriculumRepository
from usecase.dto.summary_dto import GetWeekSummariesRequest, GetWeekSummariesResponse, WeekSummaryData

class GetWeekSummariesUseCase:
    def __init__(
        self,
        summary_repository: SummaryRepository,
        week_topic_repository: WeekTopicRepository,
        curriculum_repository: CurriculumRepository
    ):
        self.summary_repository = summary_repository
        self.week_topic_repository = week_topic_repository
        self.curriculum_repository = curriculum_repository
    
    async def execute(self, request: GetWeekSummariesRequest) -> GetWeekSummariesResponse:
        # 1. 주차 정보 조회
        week_topic = await self.week_topic_repository.find_by_id(request.week_topic_id)
        if not week_topic:
            raise ValueError("주차 정보를 찾을 수 없습니다")
        
        # 2. 커리큘럼 정보 조회 및 권한 확인
        curriculum = await self.curriculum_repository.find_by_id(week_topic.curriculum_id)
        if not curriculum:
            raise ValueError("커리큘럼 정보를 찾을 수 없습니다")
        
        # 3. 권한 확인 (본인 커리큘럼 또는 공개 커리큘럼의 주차만 접근 가능)
        if curriculum.user_id != request.user_id and not curriculum.is_public:
            raise ValueError("접근 권한이 없습니다")
        
        # 4. 해당 주차의 모든 공개 요약 조회 (새로 추가한 메서드 사용!)
        summaries = await self.summary_repository.find_by_week_topic_id_and_public(
            request.week_topic_id, 
            is_public=True
        )
        
        # 5. 요약 데이터 변환
        summary_data_list = []
        for summary in summaries:
            # 내용 미리보기 생성 (앞 150자)
            content_preview = summary.content[:150] + "..." if len(summary.content) > 150 else summary.content
            
            summary_data = WeekSummaryData(
                id=summary.id,
                user_id=summary.user_id,
                content_preview=content_preview,
                created_at=summary.created_at
            )
            summary_data_list.append(summary_data)
        
        # 6. 최신순으로 정렬
        summary_data_list.sort(key=lambda x: x.created_at, reverse=True)
        
        # 7. 응답 생성
        return GetWeekSummariesResponse(
            week_topic_title=week_topic.title,
            curriculum_title=curriculum.title,
            summaries=summary_data_list
        )