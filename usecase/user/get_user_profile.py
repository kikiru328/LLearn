from domain.repositories.user_repository import UserRepository
from domain.repositories.curriculum_repository import CurriculumRepository
from domain.repositories.summary_repository import SummaryRepository
from usecase.dto.user_dto import GetUserProfileRequest, GetUserProfileResponse

class GetUserProfileUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        curriculum_repository: CurriculumRepository,
        summary_repository: SummaryRepository
    ):
        self.user_repository = user_repository
        self.curriculum_repository = curriculum_repository
        self.summary_repository = summary_repository
    
    async def execute(self, request: GetUserProfileRequest) -> GetUserProfileResponse:
        # 1. 사용자 조회
        user = await self.user_repository.find_by_id(request.user_id)
        if not user:
            raise ValueError("사용자를 찾을 수 없습니다")
        
        # 2. 통계 정보 (간단히)
        curriculums = await self.curriculum_repository.find_by_user_id(request.user_id)
        summaries = await self.summary_repository.find_by_user_id(request.user_id)
        
        # 3. 응답 생성
        return GetUserProfileResponse(
            id=user.id,
            email=user.email.value,  # Email VO의 value
            nickname=user.nickname,
            created_at=user.created_at,
            updated_at=user.updated_at,
            curriculum_count=len(curriculums),
            summary_count=len(summaries)
        )