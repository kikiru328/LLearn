class CategoryName:
    """category name"""

    __slots__ = ("_value",)

    MIN_LENGTH = 2
    MAX_LENGTH = 30

    def __init__(self, raw: str) -> None:
        if not isinstance(raw, str):  # type: ignore
            raise ValueError(f"CategoryName must be a string, got {type(raw).__name__}")

        cleaned = raw.strip()
        if not cleaned:
            raise ValueError("CategoryName cannot be empty")

        length = len(cleaned)
        if length < self.MIN_LENGTH:
            raise ValueError(
                f"CategoryName must be at least {self.MIN_LENGTH} characters"
            )
        if length > self.MAX_LENGTH:
            raise ValueError(f"CategoryName cannot exceed {self.MAX_LENGTH} characters")

        # 허용되는 문자 검사 (영문, 한글, 숫자, 공백, 하이픈)
        import re

        if not re.match(r"^[a-zA-Z0-9가-힣\s\-\.\,]+$", cleaned):
            raise ValueError(
                "CategoryName can only contain letters, numbers, spaces, and hyphens"
            )

        self._value = cleaned

    @property
    def value(self) -> str:
        return self._value

    def __eq__(self, other: object) -> bool:
        return isinstance(other, CategoryName) and self._value == other._value

    def __hash__(self) -> int:
        return hash(self._value)

    def __repr__(self) -> str:
        return f"<CategoryName {self._value!r}>"

    def __str__(self) -> str:
        return self._value
