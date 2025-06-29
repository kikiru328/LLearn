from datetime import datetime, timezone
from uuid import uuid4
from pydantic import ValidationError
import pytest

from app.schemas.summary import CreateSummaryRequest, ListSummaryResponse, SummaryResponse, UpdateSummaryRequest

VALID_SUMMARY = "주차별 요약문은 50자 이상 5000자 이하로 구성됩니다. 최소 50자 이상으로 규정한 이유는 따로 있습니다."
UPDATE_SUMMARY = "변경된 주차별 요약문 또한 50자 이상 5000자 이하로 구성됩니다. 최대 5000자 이상으로 규정한 이유는 DB 저장량 때문입니다."
class TestCreateSummaryRequest:
    def test_valid_create_summary(self):
        data = CreateSummaryRequest(
            week_topic_id=uuid4(),
            content=VALID_SUMMARY,
            is_public=False
        )
        assert data.content == VALID_SUMMARY
        assert data.is_public == False
        
    def test_default_is_public(self):
        data = CreateSummaryRequest(
            week_topic_id=uuid4(),
            content=VALID_SUMMARY
        )
        assert data.is_public == False
        
class TestUpdateSummaryRequest:
    def test_valid_total_update(self):
        data = UpdateSummaryRequest(
            week_topic_id=uuid4(),
            content=UPDATE_SUMMARY,
            is_public=True
        )
        assert data.content == UPDATE_SUMMARY
        assert data.is_public == True
        
    def test_valid_partial_update(self):
        data = UpdateSummaryRequest(
            content=UPDATE_SUMMARY,
        )
        assert data.content == UPDATE_SUMMARY
    
        data = UpdateSummaryRequest(
            is_public=True
        )
        assert data.is_public == True
            
    
    def test_invalid_update_with_short_content(self):
        with pytest.raises(ValidationError):
            UpdateSummaryRequest(
                content="짧은 요약문"
            )
            
    def test_invalid_update_with_empty_content(self):
        with pytest.raises(ValidationError):
            UpdateSummaryRequest(
                week_topic_id=uuid4(),
                content=""
            )
class TestSummaryResponse:
    def test_valid_summary_response(self):
        summary_id = uuid4()
        user_id = uuid4()
        week_topic_id = uuid4()
        now = datetime.now(timezone.utc)
        
        summary_response = SummaryResponse(
            id=summary_id,
            user_id=user_id,
            week_topic_id=week_topic_id,
            content=VALID_SUMMARY,
            is_public=False,
            created_at=now,
            updated_at=now
        )
        
        assert summary_response.id == summary_id
        assert summary_response.user_id == user_id
        assert summary_response.week_topic_id == week_topic_id
        assert summary_response.content == VALID_SUMMARY
        assert summary_response.is_public == False
        
class TestListSummaryResponse:
    def test_pagination_with_summaries(self):
        now = datetime.now(timezone.utc)
        
        def _create_summary(content):
            return SummaryResponse(
                id=uuid4(),
                user_id=uuid4(),
                week_topic_id=uuid4(),
                content=f"{VALID_SUMMARY}{content}",
                is_public=False,
                created_at=now,
                updated_at=now
            )
        summaries = [_create_summary(i) for i in range(10)]
        
        list_summaries_response = ListSummaryResponse(
            summaries=summaries,
            total=10,
            page=2,
            size=5,
            has_next=True
        )
        
        assert list_summaries_response.total == 10
        assert list_summaries_response.page == 2
        assert list_summaries_response.size == 5
        assert list_summaries_response.has_next == True
        assert list_summaries_response.summaries[0].content == f"{VALID_SUMMARY}0"
        assert list_summaries_response.summaries[5].content == f"{VALID_SUMMARY}5"
        
        