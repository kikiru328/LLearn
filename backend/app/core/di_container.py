from dependency_injector import containers, providers

from config import get_settings

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
            "user.interface.controllers",
        ]
    )

    config = providers.Singleton(get_settings)

    db_session = providers.Factory(AsyncSessionLocal)

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
