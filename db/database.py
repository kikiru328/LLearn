from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# from sqlalchemy.orm import sessionmaker
from config import get_settings


settings = get_settings()

SQLALCHEMY_DATABASE_URL = settings.sqlalchemy_database_url

engine = create_async_engine(
    settings.sqlalchemy_database_url,
    echo=True,
    future=True,
    connect_args={"charset": "utf8mb4"},
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)

Base = declarative_base()
