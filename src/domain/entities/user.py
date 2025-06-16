from dataclasses import dataclass
from uuid import UUID
from datetime import datetime    

@dataclass
class User:
    id: UUID
    email: str
    nickname: str
    hashed_password: str
    is_active: bool
    is_admin: bool
    created_at: datetime
    updated_at: datetime
    
    def change_nickname(self, new_nickname: str) -> None:
        """Change User's Nickname to new_nickname"""
        if not new_nickname or len(new_nickname.strip()) < 2:
            raise ValueError("닉네임은 2자 이상이어야 합니다.")
        self.nickname = new_nickname.strip()
        self.updated_at = datetime.now()
        
    def verify_password(self, raw_password: str, hasher) -> bool:
        """
        주입된  해시 함수(hasher)를 사용하여 비밀번호를 검증합니다.
        해시 함수는 usecase 또는 DI 컨테이너에서 주입되어야 합니다.
        """
        return hasher.verify(raw_password, self.hashed_password)
    
    def withdraw(self) -> None:
        """회원 탈퇴 처리; soft delete"""
        self.is_active = False
        self.updated_at = datetime.now()