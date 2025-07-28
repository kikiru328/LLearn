# user/application/exception.py에 추가


class PasswordTooShortError(Exception):
    def __init__(self, length: int, min_length: int):
        self.length = length
        self.min_length = min_length
        super().__init__(
            f"Password is too short. Got {length} characters, minimum {min_length} required"
        )


class PasswordTooLongError(Exception):
    def __init__(self, length: int, max_length: int):
        self.length = length
        self.max_length = max_length
        super().__init__(
            f"Password is too long. Got {length} characters, maximum {max_length} allowed"
        )


class PasswordMissingUppercaseError(Exception):
    pass


class PasswordMissingLowercaseError(Exception):
    pass


class PasswordMissingDigitError(Exception):
    pass


class PasswordMissingSpecialCharError(Exception):
    pass


class PasswordContainsWhitespaceError(Exception):
    pass
