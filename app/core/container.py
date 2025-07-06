from dependency_injector import containers, providers
from app.core.config import settings
from infrastructure.database.config import SessionLocal
from infrastructure.database.repositories.curriculum_repository_impl import CurriculumRepositoryImpl
from infrastructure.database.repositories.feedback_repository_impl import FeedbackRepositoryImpl
from infrastructure.database.repositories.summary_repository_impl import SummaryRepositoryImpl
from infrastructure.database.repositories.user_repository_impl import UserRepositoryImpl
from infrastructure.database.repositories.week_topic_repository_impl import WeekTopicRepositoryImpl
from infrastructure.services.bcrypt_password_service import BcryptPasswordService
from infrastructure.services.openai_llm_service import OpenAILLMService
from usecase.curriculum.generate_preview import GenerateCurriculumPreviewUseCase
from usecase.curriculum.get_curriculum_detail import GetCurriculumDetailUseCase
from usecase.curriculum.get_user_curriculums import GetUserCurriculumsUseCase
from usecase.curriculum.get_week_topic import GetWeekTopicUseCase
from usecase.curriculum.save_curriculum import SaveCurriculumUseCase
from usecase.feedback.generate_feedback import GenerateFeedbackUseCase
from usecase.feedback.get_feedback import GetFeedbackUseCase
from usecase.feedback.get_user_feedbacks import GetUserFeedbacksUseCase
from usecase.summary.create_summary import CreateSummaryUseCase
from usecase.summary.get_summary_detail import GetSummaryDetailUseCase
from usecase.summary.get_user_summaries import GetUserSummariesUseCase
from usecase.summary.get_week_summaries import GetWeekSummariesUseCase
from usecase.user.create_user import CreateUserUseCase
from usecase.user.get_user_profile import GetUserProfileUseCase
from usecase.user.login_user import LoginUserUseCase


class Container(containers.DeclarativeContainer):
    
    config = providers.Object(settings)
    
    # db session
    db_session = providers.Factory(SessionLocal)
    
    # service
    password_service = providers.Singleton(
        BcryptPasswordService,
    )
    
    llm_service = providers.Singleton(
        OpenAILLMService,
        api_key=config.provided.openai_api_key
    )
    
    # connect with repository & database session
    
    user_repository = providers.Factory(
        UserRepositoryImpl,
        session=db_session
    )
    
    curriculum_repository = providers.Factory(
        CurriculumRepositoryImpl,
        session=db_session
    )
    
    week_topic_repository = providers.Factory(
        WeekTopicRepositoryImpl,
        session=db_session
    )
    
    summary_repository = providers.Factory(
        SummaryRepositoryImpl,
        session=db_session
    )
    
    feedback_repository = providers.Factory(
        FeedbackRepositoryImpl,
        session=db_session
    )
    
    create_user_usecase = providers.Factory(
        CreateUserUseCase,
        user_repository=user_repository,
        password_service=password_service
    )
    
    login_user_usecase = providers.Factory(
        LoginUserUseCase,
        user_repository=user_repository,
        password_service=password_service
    )
    
    get_user_profile_usecase = providers.Factory(
        GetUserProfileUseCase,
        user_repository=user_repository,
        curriculum_repository=curriculum_repository,
        summary_repository=summary_repository
    )
    
    # === Curriculum UseCases ===
    generate_curriculum_preview_usecase = providers.Factory(
        GenerateCurriculumPreviewUseCase,
        llm_service=llm_service
    )
    
    save_curriculum_usecase = providers.Factory(
        SaveCurriculumUseCase,
        curriculum_repository=curriculum_repository,
        week_topic_repository=week_topic_repository
    )
    
    get_user_curriculums_usecase = providers.Factory(
        GetUserCurriculumsUseCase,
        curriculum_repository=curriculum_repository
    )
    
    get_curriculum_detail_usecase = providers.Factory(
        GetCurriculumDetailUseCase,
        curriculum_repository=curriculum_repository,
        week_topic_repository=week_topic_repository
    )
    
    get_week_topic_usecase = providers.Factory(
        GetWeekTopicUseCase,
        curriculum_repository=curriculum_repository,
        week_topic_repository=week_topic_repository
    )
    
    # === Summary UseCases ===
    create_summary_usecase = providers.Factory(
        CreateSummaryUseCase,
        summary_repository=summary_repository,
        week_topic_repository=week_topic_repository
    )
    
    get_user_summaries_usecase = providers.Factory(
        GetUserSummariesUseCase,
        summary_repository=summary_repository,
        week_topic_repository=week_topic_repository,
        curriculum_repository=curriculum_repository,
    )
    
    get_summary_detail_usecase = providers.Factory(
        GetSummaryDetailUseCase,
        summary_repository=summary_repository,
        week_topic_repository=week_topic_repository,
        curriculum_repository=curriculum_repository,
    )
    
    get_week_summaries_usecase = providers.Factory(
        GetWeekSummariesUseCase,
        summary_repository=summary_repository,
        week_topic_repository=week_topic_repository,
        curriculum_repository=curriculum_repository,
    )
    
    # === Feedback UseCases ===
    generate_feedback_usecase = providers.Factory(
        GenerateFeedbackUseCase,
        feedback_repository=feedback_repository,
        summary_repository=summary_repository,
        week_topic_repository=week_topic_repository,
        llm_service=llm_service
    )
    
    get_feedback_usecase = providers.Factory(
        GetFeedbackUseCase,
        feedback_repository=feedback_repository,
        summary_repository=summary_repository,
        week_topic_repository=week_topic_repository,
    )
    
    get_user_feedbacks_usecase = providers.Factory(
        GetUserFeedbacksUseCase,
        feedback_repository=feedback_repository,
        summary_repository=summary_repository,
        week_topic_repository=week_topic_repository,
        curriculum_repository=curriculum_repository
    )