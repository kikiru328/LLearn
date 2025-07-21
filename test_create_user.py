from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import asyncio
from ulid import ULID
from datetime import datetime, timezone
from faker import Faker

from user.infra.db_models.user import User as UserModel
from user.domain.entity.user import User as UserDomain
from user.domain.value_object.email import Email
from user.domain.value_object.name import Name
from utils.crypto import Crypto

from config import get_settings


settings = get_settings()

SQLALCHEMY_DATABASE_URL = settings.sqlalchemy_database_url


# Database URL - adjust as needed
DATABASE_URL = SQLALCHEMY_DATABASE_URL

# Setup AsyncSession
engine = create_async_engine(DATABASE_URL, echo=False, future=True)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)

fake = Faker()


async def seed_users(count: int = 50):
    crypto = Crypto()
    ulid_gen = ULID()
    async with AsyncSessionLocal() as session:
        added = 0
        while added < count:
            user_id = ulid_gen.generate()
            email_str = fake.unique.email()
            raw_pw = "Password123!"
            # Hash password in thread
            pw_hash = await asyncio.to_thread(crypto.encrypt, raw_pw)
            now = datetime.now(timezone.utc)

            # Generate a valid name: retry if invalid
            for _ in range(5):
                candidate = fake.first_name()  # simple alphabetic name
                try:
                    name_vo = Name(candidate)
                    break
                except ValueError:
                    continue
            else:
                # fallback to a default name
                name_vo = Name(f"user{added+1}")

            domain_user = UserDomain(
                id=user_id,
                email=Email(email_str),
                name=name_vo,
                password=pw_hash,
                created_at=now,
                updated_at=now,
            )

            # Map to ORM and add
            new_user = UserModel(
                id=domain_user.id,
                email=str(domain_user.email),
                name=str(domain_user.name),
                password=domain_user.password,
                created_at=domain_user.created_at,
                updated_at=domain_user.updated_at,
            )
            session.add(new_user)
            added += 1

        try:
            await session.commit()
            print(f"Seeded {count} users successfully.")
        except Exception as e:
            await session.rollback()
            print("Error seeding users:", e)


if __name__ == "__main__":
    asyncio.run(seed_users(50))
