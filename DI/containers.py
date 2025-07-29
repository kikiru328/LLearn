from dependency_injector import containers, providers

from config import get_settings
from curriculum.application.curriculum_service import CurriculumService
from curriculum.external.llm_client import RealLLMClient
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

    curriculum_repository = providers.Factory(
        CurriculumRepository,
        session=db_session,
    )
    summary_repository = providers.Factory(
        SummaryRepository,
        session=db_session,
    )
    feedback_repository = providers.Factory(
        FeedbackRepository,
        session=db_session,
    )

    # LLMClient 인터페이스 ↔ 구현체 매핑
    llm_client = providers.Singleton(
        RealLLMClient,
        api_key=config.provided.llm_api_key,
        endpoint=config.provided.llm_endpoint,  # implement
    )

    curriculum_service = providers.Factory(
        CurriculumService,
        curriculum_repo=curriculum_repository,
        summary_repo=summary_repository,
        feedback_repo=feedback_repository,
        llm_client=llm_client,
    )
