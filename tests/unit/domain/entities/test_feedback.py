import pytest
from datetime import datetime, timezone
from uuid import UUID, uuid4

from domain.entities.feedback import Feedback


class TestFeedback:
    """Feedback 엔티티 테스트"""

    def test_feedback_creation(self):
        """피드백 생성 테스트"""
        summary_id = uuid4()
        feedback_content = """
        ✅ 정확성 확인: 프로세스와 스레드 개념을 잘 이해하셨습니다.
        📝 누락 보충: 컨텍스트 스위칭에 대한 설명이 빠져있습니다.
        ⚠️ 오류 수정: 특별한 오류는 없습니다.
        🤔 심화 질문: 멀티프로세싱과 멀티스레딩 중 어떤 상황에서 무엇을 선택하시겠습니까?
        📚 확장 학습: 다음은 IPC(Inter-Process Communication)에 대해 학습해보세요.
        """

        feedback = Feedback(
            summary_id=summary_id,
            content=feedback_content
        )

        assert isinstance(feedback.id, UUID)
        assert feedback.summary_id == summary_id
        assert feedback.content == feedback_content
        assert isinstance(feedback.created_at, datetime)