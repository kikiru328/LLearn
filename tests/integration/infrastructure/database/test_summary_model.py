import pytest
from sqlalchemy import text
from infrastructure.database.config import sync_engine
from infrastructure.database.base import Base


class TestSummaryModel:

    @pytest.mark.skip("MySQL required. Covered by integration tests.")
    def test_database_connection(self):
        with sync_engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            assert result.fetchone()[0] == 1

    @pytest.mark.skip("MySQL required. Covered by integration tests.")
    def test_summary_table_creation(self):
        Base.metadata.create_all(bind=sync_engine)
        with sync_engine.connect() as connection:
            result = connection.execute(text("SHOW TABLES"))
            tables = [row[0] for row in result]
            assert "summaries" in tables

    @pytest.mark.skip("MySQL required. Covered by integration tests.")
    def test_summary_table_structure(self):
        Base.metadata.create_all(bind=sync_engine)
        with sync_engine.connect() as connection:
            result = connection.execute(text("DESCRIBE summaries"))
        columns = {row[0]: row[1] for row in result}

        assert "id" in columns
        assert "user_id" in columns
        assert "week_topic_id" in columns
        assert "content" in columns
        assert "is_public" in columns
