from dataclasses import dataclass

@dataclass(frozen=True)
class Password:
    hashed_value: str

    def __post_init__(self):
        # bcrypt
        if not self.hashed_value.startswith("$2b$"):
            raise ValueError("비밀번호는 반드시 hash된 값이어야 합니다.")

    def __str__(self):
        return self.hashed_value