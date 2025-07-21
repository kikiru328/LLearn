from dependency_injector import containers, providers

from config import get_settings
from db.database import AsyncSessionLocal
from user.application.user_service import UserService
from user.infra.repository.user_repo import UserRepository
from ulid import ULID

from utils.crypto import Crypto


class Container(containers.DeclarativeContainer):
    # setting
    wiring_config = containers.WiringConfiguration(
        packages=["user.interface.controllers"]
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
