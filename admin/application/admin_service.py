from user.application.user_service import UserService
from user.domain.repository.user_repo import IUserRepository
from user.domain.value_object.name import Name
from user.domain.value_object.role import RoleVO
from utils.crypto import Crypto


class AdminService:
    def __init__(
        self,
        user_service: UserService,
        user_repo: IUserRepository,
    ):

        self.user_service = user_service
        self.user_repo: IUserRepository = user_repo

    async def get_user_by_name(self, user_name: str):
        return await self.user_service.get_user_by_name(user_name)

    async def update_user(self, user_id, name, password, role):
        return await self.user_service.update_user(user_id, name, password, role)
