# user/domain/value_object/name.py
import re
from typing import Any

# 영문 대소문자·숫자·밑줄만 2~8자
_NAME_RE = re.compile(r"^[A-Za-z0-9_\uAC00-\uD7A3]{2,8}$")  # 한글 음절(가–힣) 추


class Name:
    __slots__ = ("_value",)

    def __init__(self, raw: str) -> None:
        if not isinstance(raw, str) or not _NAME_RE.fullmatch(raw):
            raise ValueError("Invalid name")
        self._value = raw  # 별도 정규화 없음 (규칙상 그대로 사용)

    def __str__(self) -> str:
        return self._value

    def __repr__(self) -> str:
        return f"<Name {self._value}>"

    def __eq__(self, other: Any) -> bool:
        return str(self) == str(other) if isinstance(other, Name) else False

    def __hash__(self) -> int:
        return hash(self._value)
