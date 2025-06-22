from dataclasses import dataclass
import re

@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.value):
            raise ValueError(f"유효하지 않은 이메일 형식입니다: {self.value}")

    def domain(self) -> str:
        return self.value.split('@')[1]

    def __str__(self):
        return self.value
