from app.core.container import Container
from infrastructure.database.repositories.user_repository_impl import UserRepositoryImpl
from infrastructure.services.bcrypt_password_service import BcryptPasswordService
from infrastructure.services.openai_llm_service import OpenAILLMService
from usecase.user.create_user import CreateUserUseCase


class TestContainer:
    def setup_method(self):
        self.container = Container()
            
    def test_config_provider(self):
            config = self.container.config()
            assert config is not None
            assert config.environment
            assert config.openai_api_key
        
    def test_service_provider_singleton(self):
        password_service1 = self.container.password_service()
        password_service2 = self.container.password_service()
        
        llm_service1 = self.container.llm_service()
        llm_service2 = self.container.llm_service()
        
        assert password_service1 is password_service2
        assert llm_service1 is llm_service2
        assert isinstance(password_service1, BcryptPasswordService)
        assert isinstance(llm_service1, OpenAILLMService)
        
    def test_repository_providers_factory(self):
        user_repo1 = self.container.user_repository()
        user_repo2 = self.container.user_repository()

        assert user_repo1 is not user_repo2
        assert isinstance(user_repo1, UserRepositoryImpl)
        assert isinstance(user_repo2, UserRepositoryImpl)
    
    def test_usecase_dependency_injection(self):
        create_user_usecase = self.container.create_user_usecase()

        assert isinstance(create_user_usecase, CreateUserUseCase)
        assert create_user_usecase.user_repository is not None
        assert create_user_usecase.password_service is not None
        
        assert isinstance(create_user_usecase.user_repository, UserRepositoryImpl)
        assert isinstance(create_user_usecase.password_service, BcryptPasswordService)
    
    def test_complex_usecase_dependency_injection(self):
        generate_feedback_usecase = self.container.generate_feedback_usecase()
        

        assert generate_feedback_usecase.feedback_repository is not None
        assert generate_feedback_usecase.summary_repository is not None
        assert generate_feedback_usecase.llm_service is not None
    
    def test_all_usecases_can_be_created(self):
        assert self.container.create_user_usecase() is not None
        assert self.container.login_user_usecase() is not None
        assert self.container.get_user_profile_usecase() is not None
        
        assert self.container.generate_curriculum_preview_usecase() is not None
        assert self.container.save_curriculum_usecase() is not None
        assert self.container.get_user_curriculums_usecase() is not None
        assert self.container.get_curriculum_detail_usecase() is not None
        assert self.container.get_week_topic_usecase() is not None
        
        assert self.container.create_summary_usecase() is not None
        assert self.container.get_user_summaries_usecase() is not None
        assert self.container.get_summary_detail_usecase() is not None
        assert self.container.get_week_summaries_usecase() is not None
        
        assert self.container.generate_feedback_usecase() is not None
        assert self.container.get_feedback_usecase() is not None
        assert self.container.get_user_feedbacks_usecase() is not None