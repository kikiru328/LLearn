from domain.services.password_service import PasswordService
import bcrypt

class BcryptPasswordService(PasswordService):
    """bycrpt 사용 password hash"""
    
    def hash_password(self, password: str) -> str:
        if not password or len(password.strip()) == 0:
            raise ValueError("비밀번호는 필수입니다")
        
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode('utf-8')
    
    def verify_password(self, password: str, hashed: str) -> bool:
        password_bytes = password.encode('utf-8')
        hashed_bytes = hashed.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_bytes)
        
