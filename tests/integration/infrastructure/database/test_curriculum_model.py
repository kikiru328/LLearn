import pytest
from sqlalchemy import text
from infrastructure.database.config import sync_engine
from infrastructure.database.base import Base
from infrastructure.database.models.curriculum_model import CurriculumModel

class TestCurriculumModel:
    """
    Curriculum SQLAlchemy Model Test

    Goal:
    - Curriculum Model이 실제 MySQL DB와 올바르게 연동되는가
    - 테이블 생성, 구조, 연결이 잘 되는지
    - FK 관계
    - 제약조건 (nullable, unique)가 잘 작동하는가
    """
    @pytest.mark.skip("MySQL required. Covered by integration tests.")
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

    @pytest.mark.skip("MySQL required. Covered by integration tests.")
    def test_curriculum_table_creation(self):
        """
        Curriculum table 생성 테스트

        goal: curriculum model class가 실제 mysql table로 생성되는지
        validation: `curriculum` table이 database에 존재하는가
        """
        Base.metadata.create_all(bind=sync_engine)
        with sync_engine.connect() as connection:
            result = connection.execute(text("SHOW TABLES"))
            tables = [row[0] for row in result]
            assert 'curriculums' in tables

    @pytest.mark.skip("MySQL required. Covered by integration tests.")
    def test_curriculum_table_structure(self):
        """
        curriculum table structure test

        goal: 생성된 table이 정의한 컬럼을 가지고 있는지
        validation: 모든 컬럼이 올바르게 생성되었는가
        """
        Base.metadata.create_all(bind=sync_engine)
        with sync_engine.connect() as connection:
            result = connection.execute(text("DESCRIBE curriculums"))

        columns = {row[0]: row[1] for row in result}

        assert "user_id" in columns
        assert "title" in columns
        assert "goal" in columns
        assert "duration_weeks" in columns
        assert "is_public" in columns