from dependency_injector import containers, providers

from app.common.llm.openai_client import OpenAILLMClient
from app.modules.curriculum.application.service.curriculum_service import (
    CurriculumService,
)
from app.modules.curriculum.domain.service.curriculum_domain_service import (
    CurriculumDomainService,
)
from app.modules.curriculum.infrastructure.repository.curriculum_repo import (
    CurriculumRepository,
)
from app.modules.user.domain.service.user_domain_service import UserDomainService
from app.core.config import get_settings

from app.common.db.database import AsyncSessionLocal
from app.modules.user.application.service.auth_service import AuthService
from app.modules.user.application.service.user_service import UserService
from app.modules.user.infrastructure.repository.user_repo import UserRepository
from ulid import ULID  # type: ignore

from app.utils.crypto import Crypto


class Container(containers.DeclarativeContainer):
    # setting
    wiring_config = containers.WiringConfiguration(
        packages=[
            "app.modules.user.interface.controller",
            "app.modules.curriculum.interface.controller",
        ]
    )

    config = providers.Singleton(get_settings)

    db_session = providers.Factory(AsyncSessionLocal)

    # User
    user_repository = providers.Factory(
        UserRepository,
        session=db_session,
    )

    user_domain_service = providers.Factory(
        UserDomainService,
        user_repo=user_repository,
    )

    user_service = providers.Factory(
        UserService,
        user_repo=user_repository,
        user_domain_service=user_domain_service,
        ulid=providers.Singleton(ULID),
        crypto=providers.Singleton(Crypto),
    )

    # Auth
    auth_service = providers.Factory(
        AuthService,
        user_repo=user_repository,
        user_domain_service=user_domain_service,
        ulid=providers.Singleton(ULID),
        crypto=providers.Singleton(Crypto),
    )

    # LLM
    llm_client = providers.Singleton(
        OpenAILLMClient,
        api_key=config.provided.llm_api_key,
    )

    # Curriculum
    curriculum_repository = providers.Factory(
        CurriculumRepository,
        session=db_session,
    )

    curriculum_domain_service = providers.Factory(
        CurriculumDomainService,
        curriculum_repo=curriculum_repository,
    )
    curriculum_service = providers.Factory(
        CurriculumService,
        curriculum_repo=curriculum_repository,
        curriculum_domain_service=curriculum_domain_service,
        llm_client=llm_client,
        ulid=providers.Singleton(ULID),
    )
