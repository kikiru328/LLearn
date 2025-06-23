import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from infrastructure.database.base import Base

@pytest_asyncio.fixture
async def test_session():
    # 매 session 마다 engine 생성 및 삭제
    test_engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=False
    )
    async with test_engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    async_session_local = async_sessionmaker(bind=test_engine)
    session = async_session_local()

    try:
        yield session  # ← 이 부분이 제대로 session 객체를 반환해야 함
    finally:
        await session.close()
        await test_engine.dispose()