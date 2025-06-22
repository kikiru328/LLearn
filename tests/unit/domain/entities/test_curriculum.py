import pytest
from datetime import datetime, timezone
from uuid import UUID, uuid4

from domain.entities.curriculum import Curriculum


class TestCurriculum:

    def test_curriculum_creation(self):
        """커리큘럼 생성 테스트"""
        user_id = uuid4()
        curriculum = Curriculum(
            user_id=user_id,
            title="CS 기초 학습",
            goal="컴퓨터 과학 기초를 익히자",
            duration_weeks=12
        )

        assert isinstance(curriculum.id, UUID)
        assert curriculum.user_id == user_id
        assert curriculum.title == "CS 기초 학습"
        assert curriculum.goal == "컴퓨터 과학 기초를 익히자"
        assert curriculum.duration_weeks == 12
        assert curriculum.is_public is False
        assert isinstance(curriculum.created_at, datetime)
        assert isinstance(curriculum.updated_at, datetime)

    def test_update_title_success(self):
        """커리큘럼 제목 수정 성공 테스트"""
        curriculum = Curriculum(
            user_id=uuid4(),
            title="원래 제목",
            goal="목표",
            duration_weeks=12
        )
        old_updated_at = curriculum.updated_at

        curriculum.update_title("새로운 제목")

        assert curriculum.title == "새로운 제목"
        assert curriculum.updated_at > old_updated_at

    def test_update_title_with_empty_string_raises_error(self):
        """커리큘럼 제목 실패 테스트: 비어 있을 경우"""
        curriculum = Curriculum(
            user_id=uuid4(),
            title="원래 제목",
            goal="목표",
            duration_weeks=12
        )

        with pytest.raises(ValueError, match="커리큘럼 제목은 2자 이상이어야 합니다"):
            curriculum.update_title("")

    def test_update_title_with_short_string_raises_error(self):
        """커리큘럼 제목 실패 테스트: 짤은 경우"""
        curriculum = Curriculum(
            user_id=uuid4(),
            title="원래 제목",
            goal="목표",
            duration_weeks=12
        )

        with pytest.raises(ValueError, match="커리큘럼 제목은 2자 이상이어야 합니다"):
            curriculum.update_title("a")

    def test_make_public(self):
        """커리큘럼 공개 테스트"""
        curriculum = Curriculum(
            user_id=uuid4(),
            title="제목",
            goal="목표",
            duration_weeks=12
        )
        old_updated_at = curriculum.updated_at

        curriculum.make_public()

        assert curriculum.is_public is True
        assert curriculum.updated_at > old_updated_at

    def test_make_private(self):
        """커리큘럼 비공개 테스트"""
        curriculum = Curriculum(
            user_id=uuid4(),
            title="제목",
            goal="목표",
            duration_weeks=12,
            is_public=True
        )
        old_updated_at = curriculum.updated_at

        curriculum.make_private()

        assert curriculum.is_public is False
        assert curriculum.updated_at > old_updated_at