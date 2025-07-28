import re


class PasswordValidator:

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

    @staticmethod
    def validate(raw: str) -> None:
        if not isinstance(raw, str):
            raise ValueError("Password must be a string")

        if not PasswordValidator._PASSWORD_RE.match(raw):
            raise ValueError(
                "Password must be 8-64 characters with uppercase, lowercase, number, and special character"
            )
