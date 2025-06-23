from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.engine import create_engine
from dotenv import load_dotenv
import os

# .env 파일 읽기
load_dotenv()

# 환경 확인
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# 환경별 설정
if ENVIRONMENT == "testing":
    DB_NAME = "llearn_test"
    DB_HOST = "localhost"  # pytest는 Docker 외부에서 실행
else:
    DB_NAME = os.getenv('MYSQL_DATABASE', 'llearn_dev')
    DB_HOST = "mysql"      # Docker 내부에서는 서비스명

# 데이터베이스 URL 만들기
DATABASE_URL = f"mysql+aiomysql://root:{os.getenv('MYSQL_ROOT_PASSWORD')}@{DB_HOST}:3306/{DB_NAME}"

# 엔진 만들기
async_engine = create_async_engine(DATABASE_URL, echo=True)

# for test in sync
sync_engine = create_engine(DATABASE_URL.replace("aiomysql", "pymysql"))

# 세션 팩토리 만들기
SessionLocal = async_sessionmaker(bind=async_engine)

# 세션 가져오는 함수
def get_db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
