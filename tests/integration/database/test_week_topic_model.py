import pytest
from sqlalchemy import text
from infrastructure.database.config import sync_engine
from infrastructure.database.base import Base
from infrastructure.database.models.week_topic_model import WeekTopicModel
from infrastructure.database.models.curriculum_model import CurriculumModel


class TestWeekTopicModel:

    @pytest.mark.skip("MySQL required. Covered by integration tests.")
    def test_database_connection(self):
        with sync_engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            assert result.fetchone()[0] == 1

    @pytest.mark.skip("MySQL required. Covered by integration tests.")
    def test_week_topic_table_creation(self):
        Base.metadata.create_all(bind=sync_engine)
        with sync_engine.connect() as connection:
            result = connection.execute(text("SHOW TABLES"))
            tables = [row[0] for row in result]
            assert 'week_topics' in tables

    @pytest.mark.skip("MySQL required. Covered by integration tests.")
    def test_week_topic_table_structure(self):
        Base.metadata.create_all(bind=sync_engine)
        with sync_engine.connect() as connection:
            result = connection.execute(text("DESCRIBE week_topics"))
            columns = {row[0]: row[1] for row in result}

            assert "curriculum_id" in columns
            assert "week_number" in columns
            assert "title" in columns
            assert "description" in columns
            assert "learning_goals" in columns