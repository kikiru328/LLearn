import pytest
from datetime import datetime
from uuid import UUID, uuid4

from domain.entities.summary import Summary


class TestSummary:
    """Summary 엔티티 테스트"""

    def test_summary_creation(self):
        """요약 생성 테스트"""
        user_id = uuid4()
        week_topic_id = uuid4()
        summary = Summary(
            user_id=user_id,
            week_topic_id=week_topic_id,
            content="이번 주에 배운 내용을 정리하면 다음과 같습니다.",
        )

        assert isinstance(summary.id, UUID)
        assert summary.user_id == user_id
        assert summary.week_topic_id == week_topic_id
        assert summary.content == "이번 주에 배운 내용을 정리하면 다음과 같습니다."
        assert summary.is_public is False
        assert isinstance(summary.created_at, datetime)
        assert isinstance(summary.updated_at, datetime)

    def test_update_content_success(self):
        """내용 변경 성공 테스트"""
        summary = Summary(
            user_id=uuid4(), week_topic_id=uuid4(), content="원래 요약 내용입니다."
        )
        old_updated_at = summary.updated_at

        summary.update_content("새로운 요약 내용으로 변경했습니다.")

        assert summary.content == "새로운 요약 내용으로 변경했습니다."
        assert summary.updated_at > old_updated_at

    def test_update_content_with_empty_string_raises_error(self):
        """내용 변경 실패 테스트: 빈 내용 제출"""
        summary = Summary(
            user_id=uuid4(), week_topic_id=uuid4(), content="원래 요약 내용입니다."
        )

        with pytest.raises(ValueError, match="요약 내용은 10자 이상이어야 합니다"):
            summary.update_content("")

    def test_update_content_with_short_string_raises_error(self):
        """내용 변경 실패 테스트: 짧은 내용 제출"""
        summary = Summary(
            user_id=uuid4(), week_topic_id=uuid4(), content="원래 요약 내용입니다."
        )

        with pytest.raises(ValueError, match="요약 내용은 10자 이상이어야 합니다"):
            summary.update_content("짧음")

    def test_make_public(self):
        """요약 공개 설정 테스트"""
        summary = Summary(
            user_id=uuid4(), week_topic_id=uuid4(), content="요약 내용입니다."
        )
        old_updated_at = summary.updated_at

        summary.make_public()

        assert summary.is_public is True
        assert summary.updated_at > old_updated_at

    def test_make_private(self):
        """요약 비공개 설정 테스트"""
        summary = Summary(
            user_id=uuid4(),
            week_topic_id=uuid4(),
            content="요약 내용입니다.",
            is_public=True,
        )
        old_updated_at = summary.updated_at

        summary.make_private()

        assert summary.is_public is False
        assert summary.updated_at > old_updated_at
