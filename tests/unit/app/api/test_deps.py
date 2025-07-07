import pytest
from unittest.mock import Mock
from app.api.deps import (
    container,
    get_create_user_usecase,
    get_login_user_usecase,
    get_user_profile_usecase, 
    
    get_generate_curriculum_preview_usecase,
    get_save_curriculum_usecase,
    get_user_curriculums_usecase,
    get_curriculum_detail_usecase,
    get_week_topic_usecase,
    
    get_create_summary_usecase,
    get_user_summaries_usecase,
    get_summary_detail_usecase,
    get_week_summaries_usecase,

    get_generate_feedback_usecase,
    get_feedback_usecase,
    get_user_feedbacks_usecase,
)

from usecase.user.create_user import CreateUserUseCase
from usecase.user.login_user import LoginUserUseCase
from usecase.user.get_user_profile import GetUserProfileUseCase

from usecase.curriculum.generate_curriculum_preview import GenerateCurriculumPreviewUseCase
from usecase.curriculum.save_curriculum import SaveCurriculumUseCase
from usecase.curriculum.get_user_curriculums import GetUserCurriculumsUseCase
from usecase.curriculum.get_curriculum_detail import GetCurriculumDetailUseCase
from usecase.curriculum.get_week_topic import GetWeekTopicUseCase

from usecase.summary.create_summary import CreateSummaryUseCase
from usecase.summary.get_summary_detail import GetSummaryDetailUseCase
from usecase.summary.get_user_summaries import GetUserSummariesUseCase
from usecase.summary.get_week_summaries import GetWeekSummariesUseCase

from usecase.feedback.generate_feedback import GenerateFeedbackUseCase
from usecase.feedback.get_feedback import GetFeedbackUseCase
from usecase.feedback.get_user_feedbacks import GetUserFeedbacksUseCase

class TestUserDependencies:
    def test_get_create_user_usecase_returns_correct_type(self):
        usecase = get_create_user_usecase()
        assert isinstance(usecase, CreateUserUseCase)
        
    def test_get_login_user_uscase_returns_correct_type(self):
        usecase = get_login_user_usecase()
        assert isinstance(usecase, LoginUserUseCase)
        
    def test_get_user_profile_usecase_returns_correct_type(self):
        usecase = get_user_profile_usecase()
        assert isinstance(usecase, GetUserProfileUseCase)
        
class TestCurriculumDependencies:
    def test_get_generate_curriculum_preview_usecase_returns_correct_type(self):
        usecase = get_generate_curriculum_preview_usecase()
        assert isinstance(usecase, GenerateCurriculumPreviewUseCase)
        
    def test_get_save_curriculum_usecase_returns_correct_type(self):
        usecase = get_save_curriculum_usecase()
        assert isinstance(usecase, SaveCurriculumUseCase)
        
    def test_get_user_curriculums_usecase_returns_correct_type(self):
        usecase = get_user_curriculums_usecase()
        assert isinstance(usecase, GetUserCurriculumsUseCase)
        
    def test_get_curriculum_detail_usecase_returns_correct_type(self):
        usecase = get_curriculum_detail_usecase()
        assert isinstance(usecase, GetCurriculumDetailUseCase)
        
    def test_get_week_topic_usecase_returns_correct_type(self):
        usecase = get_week_topic_usecase()
        assert isinstance(usecase, GetWeekTopicUseCase)
        
class TestSummaryDependencies:
    def test_get_create_summary_usecase_returns_correct_type(self):
        usecase = get_create_summary_usecase()
        assert isinstance(usecase, CreateSummaryUseCase)
        
    def test_get_user_summaries_usecase_returns_correct_type(self):
        usecase = get_user_summaries_usecase()
        assert isinstance(usecase, GetUserSummariesUseCase)
        
    def test_get_summary_detail_usecase_returns_correct_type(self):
        usecase = get_summary_detail_usecase()
        assert isinstance(usecase, GetSummaryDetailUseCase)
        
    def test_get_week_summaries_usecase_returns_correct_type(self):
        usecase = get_week_summaries_usecase()
        assert isinstance(usecase, GetWeekSummariesUseCase)
        
class TestFeedbackDependencies:
    def test_get_generate_feedback_usecase_returns_correct_type(self):
        usecase = get_generate_feedback_usecase()
        assert isinstance(usecase, GenerateFeedbackUseCase)
        
    def test_get_feedback_usecase_returns_correct_type(self):
        usecase = get_feedback_usecase()
        assert isinstance(usecase, GetFeedbackUseCase)
    
    def test_get_user_feedbacks_usecase_returns_correct_type(self):
        usecase = get_user_feedbacks_usecase()
        assert isinstance(usecase, GetUserFeedbacksUseCase)
        
        
class TestContainerIntegration:
    
    def test_user_usecases_have_proper_dependencies_injected(self):
        create_usecase = get_create_user_usecase()
        login_usecase = get_login_user_usecase()
        
        assert hasattr(create_usecase, 'user_repository')
        assert hasattr(create_usecase, 'password_service')
        assert hasattr(login_usecase, 'user_repository')
        assert hasattr(login_usecase, 'password_service')

        assert create_usecase.user_repository is not None
        assert create_usecase.password_service is not None
        assert login_usecase.user_repository is not None
        assert login_usecase.password_service is not None
    
    def test_repository_factory_pattern(self):
        """매번 새로 생성되는지"""
        usecase1 = get_create_user_usecase()
        usecase2 = get_login_user_usecase()
        assert usecase1.user_repository is not usecase2.user_repository
        
    def test_service_singleton_pattern(self):
        """service -> singleton?"""
        usecase1 = get_create_user_usecase()
        usecase2 = get_login_user_usecase()
        assert usecase1.password_service is usecase2.password_service
        
    def test_curriculum_usecases_have_proper_dependencies_injected(self):
        generate_usecase = get_generate_curriculum_preview_usecase()
        save_usecase = get_save_curriculum_usecase()
        
        assert hasattr(generate_usecase, 'llm_service')
        assert hasattr(save_usecase, 'curriculum_repository')
        assert hasattr(save_usecase, 'week_topic_repository')
        
        assert generate_usecase.llm_service is not None
        
    def test_container_mock_override_functionality(self):
        mock_user_repository = Mock()
        mock_password_service = Mock()
        with container.user_repository.override(mock_user_repository), \
             container.password_service.override(mock_password_service):
            usecase = get_create_user_usecase()
            assert usecase.user_repository is mock_user_repository
            assert usecase.password_service is mock_password_service
            
        # override 해제
        usecase_after = get_create_user_usecase()
        assert usecase_after.user_repository is not mock_user_repository
        assert usecase_after.password_service is not mock_password_service
        
    def test_multiple_usecase_mock_override(self):
        """multi usecase mock override"""
        mock_curriculum_repo = Mock()
        mock_llm_service = Mock()
        with container.curriculum_repository.override(mock_curriculum_repo), \
             container.llm_service.override(mock_llm_service):
            
            generate_usecase = get_generate_curriculum_preview_usecase()
            save_usecase = get_save_curriculum_usecase()
            
            assert generate_usecase.llm_service is mock_llm_service
            assert save_usecase.curriculum_repository is mock_curriculum_repo