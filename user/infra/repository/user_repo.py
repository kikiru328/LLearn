from typing import Optional
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from user.application.exception import UserNotFoundError
from user.domain.entity.user import User as UserDomain
from user.domain.repository.user_repo import IUserRepository
from user.domain.value_object.name import Name
from user.domain.value_object.password import Password
from user.domain.value_object.role import RoleVO
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
            password=user.password.value,  # str
            role=user.role,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
        self.session.add(new_user)
        try:
            await self.session.commit()
        except:
            await self.session.rollback()
            raise

    async def find_by_id(self, id: str) -> Optional[UserDomain]:

        user = await self.session.get(UserModel, id)

        if not user:
            return None  # 없으면 none

        return UserDomain(
            id=user.id,
            email=Email(user.email),
            name=Name(user.name),
            password=Password(user.password),  # domain password: VO
            role=RoleVO(user.role),
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

    async def find_by_email(self, email: Email) -> Optional[UserDomain]:

        query = select(UserModel).where(UserModel.email == str(email))
        response = await self.session.execute(query)
        user = response.scalars().first()

        if not user:
            return None

        return UserDomain(
            id=user.id,
            email=Email(user.email),
            name=Name(user.name),
            password=Password(user.password),
            role=RoleVO(user.role),
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

    async def find_by_name(self, name: Name) -> Optional[UserDomain]:

        query = select(UserModel).where(UserModel.name == str(name))
        response = await self.session.execute(query)
        user = response.scalars().first()

        if not user:
            return None

        return UserDomain(
            id=user.id,
            email=Email(user.email),
            name=Name(user.name),
            password=Password(user.password),
            role=RoleVO(user.role),
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

    async def find_users(
        self,
        page: int = 1,
        items_per_page: int = 10,
    ) -> tuple[int, list[UserDomain]]:

        # total count
        count_query = select(func.count()).select_from(UserModel)
        count_result = await self.session.execute(count_query)
        total_count = count_result.scalar_one()

        # paging
        offset = (page - 1) * items_per_page

        query = select(UserModel).offset(offset).limit(items_per_page)
        result = await self.session.execute(query)
        user_models = result.scalars().all()
        users = [
            UserDomain(
                id=user_model.id,
                email=Email(user_model.email),
                name=Name(user_model.name),
                password=Password(user_model.password),
                role=RoleVO(user_model.role),
                created_at=user_model.created_at,
                updated_at=user_model.updated_at,
            )
            for user_model in user_models
        ]
        return (total_count, users)

    async def update(self, user: UserDomain):

        existing_user: UserModel | None = await self.session.get(
            UserModel, user.id
        )  # find by id

        if not existing_user:
            raise UserNotFoundError(f"user with id={user.id} not found")

        existing_user.name = str(user.name)
        existing_user.password = user.password.value  # str
        existing_user.role = user.role
        existing_user.updated_at = user.updated_at

        self.session.add(existing_user)
        try:
            await self.session.commit()
        except:
            await self.session.rollback()
            raise

    async def delete(self, id: str) -> None:
        existing_user: UserModel | None = await self.session.get(
            UserModel, id
        )  # find by id
        if not existing_user:
            raise UserNotFoundError(f"user with id={id} not found")

        await self.session.delete(existing_user)

        try:
            await self.session.commit()
        except:
            await self.session.rollback()
            raise
