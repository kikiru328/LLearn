import pytest
from sqlalchemy import text
from sqlalchemy.dialects.mssql.information_schema import columns

from infrastructure.database.base import Base
from infrastructure.database.config import sync_engine


class TestFeedbackModel:

    @pytest.mark.skip("MySQL required. Covered by integration tests.")
    def test_database_connection(self):
        with sync_engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            assert result.fetchone()[0] == 1

    @pytest.mark.skip("MySQL required. Covered by integration tests.")
    def test_feedback_table_creation(self):
        Base.metadata.create_all(bind=sync_engine)
        with sync_engine.connect() as connection:
            result = connection.execute(text("SHOW TABLES"))
            tables = [row[0] for row in result]
            assert 'feedbacks' in tables

    @pytest.mark.skip("MySQL required. Covered by integration tests.")
    def test_feedback_table_structure(self):
        Base.metadata.create_all(bind=sync_engine)
        with sync_engine.connect() as connection:
            result = connection.execute(text("DESCRIBE feedbacks"))

        columns = {row[0]: row[1] for row in result}

        assert "summary_id" in columns
        assert "content" in columns