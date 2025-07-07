from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.engine import create_engine
from app.core.config import settings
import os


# 환경 확인
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# 환경별 설정
if ENVIRONMENT == "testing":
    DB_NAME = "llearn_test"
    DATABASE_URL = f"mysql+pymysql://root:{os.getenv('MYSQL_ROOT_PASSWORD')}@localhost:3306/llearn_test"
    sync_engine = create_engine(DATABASE_URL.replace("aiomysql", "pymysql"))
    async_engine = None
    SessionLocal = None
else:
    DATABASE_URL = settings.database_url
    async_database_url = DATABASE_URL.replace("pymysql", "aiomysql")

    # 비동기 엔진 생성
    async_engine = create_async_engine(async_database_url, echo=True)
    sync_engine = create_engine(DATABASE_URL)
    SessionLocal = async_sessionmaker(bind=async_engine)  # Docker 내부에서는 서비스명

# 세션 가져오는 함수


def get_db_session():
    if ENVIRONMENT == "testing":
        from sqlalchemy.orm import sessionmaker

        TestSession = sessionmaker(bind=sync_engine)
        session = TestSession()
    else:
        session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
