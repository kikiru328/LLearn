import pytest
from datetime import datetime, timezone
from uuid import UUID, uuid4

from domain.entities.week_topic import WeekTopic


class TestWeekTopic:

    def test_week_topic_creation(self):
        """주차별 커리큘럼 생성 테스트"""
        curriculum_id = uuid4()
        week_topic = WeekTopic(
            curriculum_id=curriculum_id,
            week_number=1,
            title="컴퓨터 구조 기초",
            description="CPU, 메모리, 입출력 장치에 대해 학습합니다",
            learning_goals=["CPU 작동 원리 이해", "메모리 계층 구조 학습"]
        )

        assert isinstance(week_topic.id, UUID)
        assert week_topic.curriculum_id == curriculum_id
        assert week_topic.week_number == 1
        assert week_topic.title == "컴퓨터 구조 기초"
        assert week_topic.description == "CPU, 메모리, 입출력 장치에 대해 학습합니다"
        assert week_topic.learning_goals == ["CPU 작동 원리 이해", "메모리 계층 구조 학습"]
        assert isinstance(week_topic.updated_at, datetime)

    def test_update_title_success(self):
        """주차별 제목 수정 성공 테스트"""
        week_topic = WeekTopic(
            curriculum_id=uuid4(),
            week_number=1,
            title="원래 제목",
            description="설명",
            learning_goals=["목표1"]
        )
        old_updated_at = week_topic.updated_at

        week_topic.update_title("새로운 제목")

        assert week_topic.title == "새로운 제목"
        assert week_topic.updated_at > old_updated_at

    def test_update_title_with_empty_string_sets_default(self):
        """빈 문자열 입력시 기본값으로 설정되는 테스트"""
        week_topic = WeekTopic(
            curriculum_id=uuid4(),
            week_number=3, # 테스트 예상: "3주차"
            title="원래 제목",
            description="설명",
            learning_goals=["목표1"]
        )
        week_topic.update_title("") #빈칸
        assert week_topic.title == "3주차"

    def test_update_description_success(self):
        """설명 변경 성공 테스트"""
        week_topic = WeekTopic(
            curriculum_id=uuid4(),
            week_number=1,
            title="제목",
            description="원래 설명입니다",
            learning_goals=["목표1"]
        )
        old_updated_at = week_topic.updated_at

        # 10자 이상으로 수정
        week_topic.update_description("새로운 설명입니다 추가내용")

        assert week_topic.description == "새로운 설명입니다 추가내용"
        assert week_topic.updated_at > old_updated_at

    def test_update_description_with_empty_string_success(self):
        """설명 변경 성공 테스트: 빈 문자열"""
        week_topic = WeekTopic(
            curriculum_id=uuid4(),
            week_number=1,
            title="제목",
            description="원래 설명입니다",
            learning_goals=["목표1"]
        )
        week_topic.update_description("")
        assert week_topic.description == ""

    def test_update_learning_goals_success(self):
        """주차별 목표 수정 성공 테스트"""
        week_topic = WeekTopic(
            curriculum_id=uuid4(),
            week_number=1,
            title="제목",
            description="설명입니다",
            learning_goals=["원래 목표1", "원래 목표2"]
        )
        old_updated_at = week_topic.updated_at
        new_goals = ["새 목표1", "새 목표2", "새 목표3"]

        week_topic.update_learning_goals(new_goals)

        assert week_topic.learning_goals == new_goals
        assert week_topic.updated_at > old_updated_at

    def test_update_learning_goals_with_empty_list_raises_error(self):
        """주차별 목표 수정 실패 테스트: 아무것도 없을 경우"""
        week_topic = WeekTopic(
            curriculum_id=uuid4(),
            week_number=1,
            title="제목",
            description="설명입니다",
            learning_goals=["목표1"]
        )

        with pytest.raises(ValueError, match="학습 내용은 최소 1개 이상이어야 합니다"):
            week_topic.update_learning_goals([])