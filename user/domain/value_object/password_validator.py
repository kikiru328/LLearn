import re
from user.application.password_exception import (
    PasswordTooShortError,
    PasswordTooLongError,
    PasswordMissingUppercaseError,
    PasswordMissingLowercaseError,
    PasswordMissingDigitError,
    PasswordMissingSpecialCharError,
    PasswordContainsWhitespaceError,
)


class PasswordValidator:
    MIN_LENGTH = 8
    MAX_LENGTH = 64

    @staticmethod
    def validate(raw: str) -> None:
        if not isinstance(raw, str):
            raise ValueError("Password must be a string")

        # 1. 길이 검증
        if len(raw) < PasswordValidator.MIN_LENGTH:
            raise PasswordTooShortError(len(raw), PasswordValidator.MIN_LENGTH)

        if len(raw) > PasswordValidator.MAX_LENGTH:
            raise PasswordTooLongError(len(raw), PasswordValidator.MAX_LENGTH)

        # 2. 공백 검증
        if " " in raw or "\t" in raw or "\n" in raw or "\r" in raw:
            raise PasswordContainsWhitespaceError()

        # 3. 대문자 검증
        if not re.search(r"[A-Z]", raw):
            raise PasswordMissingUppercaseError()

        # 4. 소문자 검증
        if not re.search(r"[a-z]", raw):
            raise PasswordMissingLowercaseError()

        # 5. 숫자 검증
        if not re.search(r"\d", raw):
            raise PasswordMissingDigitError()

        # 6. 특수문자 검증
        if not re.search(r"[^A-Za-z0-9]", raw):
            raise PasswordMissingSpecialCharError()
