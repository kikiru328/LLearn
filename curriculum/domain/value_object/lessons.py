from typing import List, Any


class Lessons:
    """
    한 주차 내 세부 커리큘럼 항목들을 표현하는 VO.
    1개 이상, 최대 5개까지의 non-empty 문자열 리스트만 허용합니다.
    """

    __slots__ = ("_items",)

    MIN_COUNT = 1
    MAX_COUNT = 5

    def __init__(self, raw: List[Any]) -> None:
        # 1) 타입 검사
        if not isinstance(raw, list):
            raise ValueError(f"Lessons must be a list, got {type(raw).__name__}")

        # 2) 항목별 strip() 및 빈 값 제거
        cleaned: List[str] = []
        for i, item in enumerate(raw):
            if not isinstance(item, str):
                raise ValueError(
                    f"Lesson at index {i} must be a string, got {type(item).__name__}"
                )
            text = item.strip()
            if text:
                cleaned.append(text)

        count = len(cleaned)
        # 3) 개수 검증
        if count < self.MIN_COUNT:
            raise ValueError("Lessons cannot be empty")
        if count > self.MAX_COUNT:
            raise ValueError(
                f"Lessons cannot exceed {self.MAX_COUNT} items (got {count})"
            )

        # 4) 불변 저장
        self._items = tuple(cleaned)

    @property
    def items(self) -> List[str]:
        return list(self._items)

    @property
    def count(self) -> int:
        return len(self._items)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Lessons) and self._items == other._items

    def __hash__(self) -> int:
        return hash(self._items)

    def __repr__(self) -> str:
        return f"<Lessons {self._items}>"
