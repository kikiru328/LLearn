from passlib.context import CryptContext


class Crypto:
    def __init__(self):
        self.password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def encrypt(self, secret):
        return self.password_context.hash(secret)

    def verify(self, secret, hash):
        return self.password_context.verify(secret, hash)
