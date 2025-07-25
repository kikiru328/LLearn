from typing import Any


class Title:
    __slots__ = ("_value",)

    def __init__(self, raw: str) -> None:
        if not isinstance(raw, str):
            raise ValueError("Title Must in Str")

        cleaned = raw.strip()

        if not cleaned:
            raise ValueError("Title은 공백으로만 이루어질 수 없습니다.")

        length = len(cleaned)
        if length < 1 or length > 50:
            raise ValueError(
                f"Title 길이는 최소 1자 이상, 50자 이하입니다. 현재: {length}"
            )

        self._value: str = cleaned

    def __str__(self) -> str:
        return self._value

    def __repr__(self) -> str:
        return f"<Title {self._value}"

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, str):
            return self._value == other
        return False

    def __hash__(self) -> int:
        return hash(self._value)

    @property
    def value(self) -> str:
        return self._value
