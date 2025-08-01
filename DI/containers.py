from dependency_injector import containers, providers

from config import get_settings

from curriculum.application.curriculum_service import CurriculumService
from curriculum.application.feedback_service import FeedbackService
from curriculum.application.summary_service import SummaryService
from curriculum.infra.llm.openai_client import OpenAILLMClient
from curriculum.infra.repository.curriculum_repo import CurriculumRepository
from curriculum.infra.repository.feedback_repo import FeedbackRepository
from curriculum.infra.repository.summary_repo import SummaryRepository
from db.database import AsyncSessionLocal
from user.application.auth_service import AuthService
from user.application.user_service import UserService
from user.infra.repository.user_repo import UserRepository
from ulid import ULID

from utils.crypto import Crypto


class Container(containers.DeclarativeContainer):
    # setting
    wiring_config = containers.WiringConfiguration(
        packages=[
            "user.interface.controllers",
            "curriculum.interface.controllers",
            "admin.interface.controllers",
        ]
    )

    config = providers.Singleton(get_settings)

    db_session = providers.Factory(AsyncSessionLocal)

    # LLM
    llm_client = providers.Singleton(
        OpenAILLMClient,
        api_key=config.provided.llm_api_key,
        endpoint=config.provided.llm_endpoint,
    )

    # User
    user_repository = providers.Factory(
        UserRepository,
        session=db_session,
    )

    user_service = providers.Factory(
        UserService,
        user_repo=user_repository,
        ulid=providers.Singleton(ULID),
        crypto=providers.Singleton(Crypto),
    )

    auth_service = providers.Factory(
        AuthService,
        user_repo=user_repository,
        ulid=providers.Singleton(ULID),
        crypto=providers.Singleton(Crypto),
    )

    # Curriculum
    curriculum_repository = providers.Factory(
        CurriculumRepository,
        session=db_session,
    )

    curriculum_service = providers.Factory(
        CurriculumService,
        curriculum_repo=curriculum_repository,
        llm_client=llm_client,
        ulid=providers.Singleton(ULID),
    )

    # Summary

    summary_repository = providers.Factory(
        SummaryRepository,
        session=db_session,
    )

    feedback_repository = providers.Factory(
        FeedbackRepository,
        session=db_session,
    )

    summary_service = providers.Factory(
        SummaryService,
        summary_repo=summary_repository,
        curriculum_repo=curriculum_repository,
        feedback_repo=feedback_repository,
        ulid=providers.Singleton(ULID),
    )

    # Feedback

    feedback_service = providers.Factory(
        FeedbackService,
        feedback_repo=feedback_repository,
        summary_repo=summary_repository,
        curriculum_repo=curriculum_repository,
        llm_client=llm_client,
        ulid=providers.Singleton(ULID),
    )
