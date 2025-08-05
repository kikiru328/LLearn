import re
from typing import List


class TagName:
    """tag name"""

    __slots__ = ("_value",)

    MIN_LENGTH = 1
    MAX_LENGTH = 20

    def __init__(self, raw: str) -> None:
        if not isinstance(raw, str):  # type: ignore
            raise ValueError(f"TagName must be a string, got {type(raw).__name__}")

        cleaned = raw.strip().lower()  # 소문자로 정규화
        if not cleaned:
            raise ValueError("TagName cannot be empty")

        length = len(cleaned)
        if length < self.MIN_LENGTH:
            raise ValueError(f"TagName must be at least {self.MIN_LENGTH} character")
        if length > self.MAX_LENGTH:
            raise ValueError(f"TagName cannot exceed {self.MAX_LENGTH} characters")

        # 허용되는 문자 검사 (영문, 한글, 숫자만, 공백 불허)

        if not re.match(r"^[a-zA-Z0-9가-힣]+$", cleaned):
            raise ValueError("TagName can only contain letters and numbers (no spaces)")

        self._value = cleaned

    @property
    def value(self) -> str:
        return self._value

    def __eq__(self, other: object) -> bool:
        return isinstance(other, TagName) and self._value == other._value

    def __hash__(self) -> int:
        return hash(self._value)

    def __repr__(self) -> str:
        return f"<TagName {self._value!r}>"

    def __str__(self) -> str:
        return self._value

    @classmethod
    def from_list(cls, tag_names: List[str]) -> List["TagName"]:
        """Generate Tag name list from name"""
        return [cls(name) for name in tag_names if name.strip()]
