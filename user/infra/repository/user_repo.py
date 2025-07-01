from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from user.application.exception import UserNotFoundError
from user.domain.entity.user import User as UserDomain
from user.domain.repository.user_repo import IUserRepository
from user.domain.value_object.name import Name
from user.infra.db_models.user import User as UserModel

from user.domain.value_object.email import Email


class UserRepository(IUserRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, user: UserDomain):
        new_user = UserModel(
            id=user.id,
            email=str(user.email),
            name=str(user.name),
            password=user.password,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
        self.session.add(new_user)
        try:
            await self.session.commit()
        except:
            await self.session.rollback()
            raise

    async def update(self, user: UserDomain):
        existing_user: UserModel | None = await self.session.get(
            UserModel, user.id
        )  # find by id
        if not existing_user:
            raise UserNotFoundError(f"user with id={user.id} not found")

        existing_user.name = str(user.name)
        existing_user.password = user.password
        existing_user.updated_at = user.updated_at

        self.session.add(existing_user)
        try:
            await self.session.commit()
        except:
            await self.session.rollback()
            raise

    async def find_by_id(self, id: str) -> UserDomain | None:
        user = await self.session.get(UserModel, id)
        if not user:
            raise UserNotFoundError(f"user with id = {id} not found")  # 없으면 none
        return UserDomain(
            id=user.id,
            email=Email(user.email),
            name=Name(user.name),
            password=user.password,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

    async def find_by_email(self, email: Email) -> UserDomain | None:
        query = select(UserModel).where(UserModel.email == str(email))
        response = await self.session.execute(query)
        user = response.scalars().first()
        if not user:
            raise UserNotFoundError(f"user with email={email} not found")  # 없으면 none
        return UserDomain(
            id=user.id,
            email=Email(user.email),
            name=Name(user.name),
            password=user.password,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
