# tests/user/infra/test_user_repository.py
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from db.database import Base
from user.infra.repository.user_repo import UserRepository
from user.domain.entity.user import User as DomainUser
from user.domain.value_object.email import Email
from user.domain.value_object.name import Name
from datetime import datetime, timezone


@pytest_asyncio.fixture(scope="module")  # 수정: pytest_asyncio.fixture 사용
async def sqlite_session():
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=False,
        future=True,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    AsyncSessionLocal = async_sessionmaker(
        engine,
        expire_on_commit=False,
    )
    async_session = AsyncSessionLocal()
    yield async_session
    await async_session.close()
    await engine.dispose()


@pytest.mark.asyncio
async def test_save_and_find(sqlite_session: AsyncSession):
    repo = UserRepository(sqlite_session)
    now = datetime.now(timezone.utc)
    domain_user = DomainUser(
        id="01TESTID000000000000000000",
        email=Email("foo@bar.com"),
        name=Name("테스트"),
        password="hashedpwd",
        created_at=now,
        updated_at=now,
    )

    # save
    await repo.save(domain_user)

    # find by email
    found = await repo.find_by_email(domain_user.email)
    assert found is not None
    assert found.id == domain_user.id
    assert str(found.email) == "foo@bar.com"
    assert str(found.name) == "테스트"

    # find by id
    found2 = await repo.find_by_id(domain_user.id)
    assert found2 and found2.email == domain_user.email


@pytest.mark.asyncio
async def test_duplicate_email_raises(sqlite_session: AsyncSession):
    repo = UserRepository(sqlite_session)
    now = datetime.now(timezone.utc)
    u1 = DomainUser("01ID1", Email("dup@dup.com"), Name("User1"), "pwd", now, now)
    u2 = DomainUser("01ID2", Email("dup@dup.com"), Name("User2"), "pwd", now, now)

    await repo.save(u1)
    with pytest.raises(Exception):
        # SQLAlchemyIntegrityError or similar
        await repo.save(u2)
