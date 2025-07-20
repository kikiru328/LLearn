# user/domain/value_object/password.py
import re
from typing import Any

# 조건:
# - 길이 8‒64
# - 대문자 1+ / 소문자 1+ / 숫자 1+ / 특수문자 1+ (공백 불가)
_PASSWORD_RE = re.compile(
    r"""
    ^(?=.*[A-Z])          # 대문자
     (?=.*[a-z])          # 소문자
     (?=.*\d)             # 숫자
     (?=.*[^A-Za-z0-9])   # 특수문자 (공백 제외)
     [^\s]{8,64}$         # 전체 길이 및 공백 금지
    """,
    re.VERBOSE,
)


class Password:
    """Raw 패스워드 검증 전용 VO.
    해싱은 utils.crypto 계층에서 수행한다.
    """

    __slots__ = ("_raw",)

    def __init__(self, raw: str) -> None:
        if not isinstance(raw, str) or not _PASSWORD_RE.match(raw):
            raise ValueError("Invalid password format")
        self._raw = raw

    @property
    def raw(self) -> str:  # 해시 전 원문 접근 (필요 시)
        return self._raw

    def __str__(self) -> str:
        return self._raw

    def __repr__(self) -> str:
        return "<Password ****>"

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Password) and self._raw == other._raw

    def __hash__(self) -> int:
        return hash(self._raw)
