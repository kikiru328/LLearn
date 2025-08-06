# tests/user/infra/test_user_repository.py
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from db.database import Base
from user.application.exception import UserNotFoundError
from user.domain.value_object.role import RoleVO
from user.infra.repository.user_repo import UserRepository
from user.infra.db_models.user import User as DBUser
from user.domain.entity.user import User as DomainUser
from user.domain.value_object.email import Email
from user.domain.value_object.name import Name
from datetime import datetime, timedelta, timezone


# @pytest_asyncio.fixture(scope="module")  # 수정: pytest_asyncio.fixture 사용
@pytest_asyncio.fixture
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
        role=RoleVO.USER,
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
    u1 = DomainUser(
        "01ID1",
        Email("dup@dup.com"),
        Name("User1"),
        "pwd",
        RoleVO.USER,
        now,
        now,
    )
    u2 = DomainUser(
        "01ID2",
        Email("dup@dup.com"),
        Name("User2"),
        "pwd",
        RoleVO.USER,
        now,
        now,
    )

    await repo.save(u1)
    with pytest.raises(Exception):
        # SQLAlchemyIntegrityError or similar
        await repo.save(u2)


@pytest.mark.asyncio
async def test_update_persists_changes(sqlite_session: AsyncSession):
    repo = UserRepository(sqlite_session)
    now = datetime.now(timezone.utc)

    # 1) 직접 DBUser 삽입
    db_user = DBUser(
        id="01UPD",
        email=str(Email("u@u.com")),
        name=str(Name("XYZABC")),
        password="PASs1234!@#$",
        role=RoleVO.USER.value,
        created_at=now,
        updated_at=now,
    )
    sqlite_session.add(db_user)
    await sqlite_session.commit()

    # 2) 도메인으로 로드 후 변경
    domain = await repo.find_by_id("01UPD")
    assert domain is not None
    domain.role = RoleVO.ADMIN
    domain.updated_at = now + timedelta(hours=1)

    # 3) 업데이트 호출
    await repo.update(domain)

    # 4) 재조회
    reloaded = await repo.find_by_id("01UPD")
    assert reloaded is not None
    assert reloaded.role == RoleVO.ADMIN
    assert reloaded.updated_at > now


@pytest.mark.asyncio
async def test_update_not_found_raises(sqlite_session: AsyncSession):
    repo = UserRepository(sqlite_session)
    now = datetime.now(timezone.utc)

    fake = DBUser(
        id="NOEXIST",
        email=str(Email("x@x.com")),
        name=str(Name("XYZABC")),
        password="PASs1234!@#$",
        role=RoleVO.USER.value,
        created_at=now,
        updated_at=now,
    )
    with pytest.raises(UserNotFoundError):
        await repo.update(fake)


@pytest.mark.asyncio
async def test_delete_and_not_found(sqlite_session: AsyncSession):
    repo = UserRepository(sqlite_session)
    now = datetime.now(timezone.utc)

    # 1) DBUser 삽입
    db_user = DBUser(
        id="01DEL",
        email=str(Email("d@d.com")),
        name=str(Name("ABCDEF")),
        password="PASs1234!@#$",
        role=RoleVO.USER.value,
        created_at=now,
        updated_at=now,
    )
    sqlite_session.add(db_user)
    await sqlite_session.commit()

    # 2) 정상 삭제 후 조회 예외
    await repo.delete("01DEL")
    with pytest.raises(UserNotFoundError):
        await repo.find_by_id("01DEL")

    # 3) 없는 ID 삭제 시 예외
    with pytest.raises(UserNotFoundError):
        await repo.delete("NO_SUCH_ID")


@pytest.mark.asyncio
async def test_find_users_paging(sqlite_session: AsyncSession):
    repo = UserRepository(sqlite_session)
    now = datetime.now(timezone.utc)

    # 1) 25명 DBUser 삽입
    for i in range(25):
        u = DBUser(
            id=f"01ID{i:02d}",
            email=str(Email(f"user{i}@test.com")),
            name=str(Name(f"User{i}")),
            password="PASs1234!@#$",
            role=RoleVO.USER.value,
            created_at=now,
            updated_at=now,
        )
        sqlite_session.add(u)
    await sqlite_session.commit()

    # 2) 페이징 검증
    total1, page1 = await repo.find_users(page=1, items_per_page=10)
    assert total1 == 25
    assert len(page1) == 10
    assert page1[0].id == "01ID00"
    assert page1[-1].id == "01ID09"

    total2, page2 = await repo.find_users(page=2, items_per_page=10)
    assert total2 == 25
    assert len(page2) == 10
    assert page2[0].id == "01ID10"
    assert page2[-1].id == "01ID19"

    total3, page3 = await repo.find_users(page=3, items_per_page=10)
    assert total3 == 25
    assert len(page3) == 5
    assert page3[0].id == "01ID20"
    assert page3[-1].id == "01ID24"
