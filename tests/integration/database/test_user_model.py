from sqlalchemy import text
from infrastructure.database.config import sync_engine
from infrastructure.database.base import Base


class TestUserModel:
    """
    User SQLAlchemy 모델 통합 테스트 클래스

    목적:
    - User 모델이 실제 MySQL DB와 올바르게 연동되는지 확인
    - 테이블 생성, 구조, 연결 등 전반적인 DB 동작 검증
    """

    def test_database_connection(self):
        """
        데이터베이스 연결 테스트

        목적: SQLAlchemy 엔진이 MySQL에 제대로 연결되는지 확인
        검증: SELECT 1 쿼리가 성공적으로 실행되는지
        """
        # with 문: 연결 자동 관리 (try-finally와 유사)
        with sync_engine.connect() as connection:
            # text(): SQLAlchemy 2.0에서 raw SQL 실행 시 필수
            result = connection.execute(text("SELECT 1"))

            # fetchone(): 결과 한 행 가져오기
            # [0]: 첫 번째 컬럼 값 (이 경우 1)
            assert result.fetchone()[0] == 1
            # 검증: 1이 반환되면 연결 성공!

    def test_user_table_creation(self):
        """
        User 테이블 생성 테스트

        목적: UserModel 클래스가 실제 MySQL 테이블로 생성되는지 확인
        검증: 'users' 테이블이 데이터베이스에 존재하는지
        """
        # Base.metadata.create_all():
        # - 모든 모델(UserModel 등)을 실제 테이블로 생성
        # - 이미 존재하면 무시 (IF NOT EXISTS와 유사)
        Base.metadata.create_all(bind=sync_engine)

        # 생성된 테이블 목록 확인
        with sync_engine.connect() as connection:
            # SHOW TABLES: MySQL 명령어로 모든 테이블 조회
            result = connection.execute(text("SHOW TABLES"))

            # 결과를 리스트로 변환
            # row[0]: 각 행의 첫 번째 컬럼 (테이블명)
            tables = [row[0] for row in result]

            # 검증: 'users' 테이블이 생성됐는지 확인
            assert 'users' in tables

    def test_user_table_structure(self):
        """
        User 테이블 구조 테스트

        목적: 생성된 테이블이 우리가 정의한 컬럼들을 가지고 있는지 확인
        검증: 모든 필수 컬럼들이 올바르게 생성됐는지
        """
        # 먼저 테이블 생성
        Base.metadata.create_all(bind=sync_engine)

        with sync_engine.connect() as connection:
            # DESCRIBE users: MySQL 명령어로 테이블 구조 조회
            # 결과: 컬럼명, 타입, NULL 허용 여부 등
            result = connection.execute(text("DESCRIBE users"))

            # 딕셔너리로 변환: {컬럼명: 타입}
            # row[0]: 컬럼명, row[1]: 데이터 타입
            columns = {row[0]: row[1] for row in result}

            # 검증: UserModel에서 정의한 모든 컬럼이 존재하는지

            # BaseModel에서 상속받은 컬럼들
            assert 'id' in columns          # UUID 기본키
            assert 'created_at' in columns  # 생성 시간
            assert 'updated_at' in columns  # 수정 시간

            # UserModel에서 정의한 컬럼들
            assert 'email' in columns        # 이메일 (유니크)
            assert 'nickname' in columns     # 닉네임
            assert 'hashed_password' in columns  # 해시된 비밀번호
            assert 'is_active' in columns    # 활성 상태
            assert 'is_admin' in columns     # 관리자 여부
            