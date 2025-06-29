from datetime import datetime, timezone
from uuid import uuid4

from app.schemas.feedback import FeedbackResponse, FeedbackWithSummaryResponse, ListFeedbackResponse
from app.schemas.summary import SummaryResponse

class TestFeedbackResponse:
    def test_valid_feedback_response(self):
        feedback_id = uuid4()
        summary_id = uuid4()
        now = datetime.now(timezone.utc)
        
        feedback = FeedbackResponse(
            id=feedback_id,
            summary_id=summary_id,
            content="요약문에 대한 피드백",
            created_at=now
        )
        
        assert feedback.id == feedback_id
        assert feedback.summary_id == summary_id
        assert feedback.content == "요약문에 대한 피드백"
        
class TestListFeedbackResponse:
    def test_pagination_with_feedbacks(self):
        now = datetime.now(timezone.utc)
        
        def _create_feedback(content):
            return FeedbackResponse(
                id=uuid4(),
                summary_id=uuid4(),
                content=content,
                created_at=now
            )
        
        feedbacks = [_create_feedback(str(i)) for i in range(10)]
        
        list_feedbacks_response = ListFeedbackResponse(
            feedbacks=feedbacks,
            total=len(feedbacks),
            page=2,
            size=5,
            has_next=True            
        )
        
        assert list_feedbacks_response.total == 10
        assert list_feedbacks_response.page == 2
        assert list_feedbacks_response.size == 5
        assert list_feedbacks_response.has_next == True
        assert list_feedbacks_response.feedbacks[0].content == "0"
        assert list_feedbacks_response.feedbacks[3].content == "3"

class TestFeedbackWithSummaryResponse:
    def test_feedback_with_summary(self):
        feedback_id = uuid4()
        summary_id = uuid4()
        user_id = uuid4()
        week_topic_id = uuid4()
        VALID_SUMMARY = "주차별 요약문은 50자 이상 5000자 이하로 구성됩니다. 최소 50자 이상으로 규정한 이유는 따로 있습니다."
        now = datetime.now(timezone.utc)
        
        feedback = FeedbackResponse(
            id=feedback_id,
            summary_id=summary_id,
            content="5단계 구조화된 피드백",
            created_at=now
        )
        
        summary = SummaryResponse(
            id=summary_id,
            user_id=user_id,
            week_topic_id=week_topic_id,
            content=VALID_SUMMARY,
            is_public=False,
            created_at=now,
            updated_at=now
        )
        
        group_feedback_summary = FeedbackWithSummaryResponse(
            feedback=feedback,
            summary=summary
        )
        
        assert group_feedback_summary.feedback.id == feedback_id
        assert group_feedback_summary.feedback.summary_id == summary_id
        assert group_feedback_summary.feedback.content == "5단계 구조화된 피드백"
        assert group_feedback_summary.summary.id == summary_id
        assert group_feedback_summary.summary.user_id == user_id
        assert group_feedback_summary.summary.week_topic_id == week_topic_id
        assert group_feedback_summary.summary.content == VALID_SUMMARY
        assert group_feedback_summary.summary.is_public == False
        