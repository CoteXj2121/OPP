import hashlib
import secrets


class PasswordHasher:
    def hash_password(self, plain: str) -> str:
        return hashlib.sha256(plain.encode()).hexdigest()

    def check_password(self, plain: str, hashed: str) -> bool:
        return self.hash_password(plain) == hashed


class TokenGenerator:
    def generate(self) -> str:
        return secrets.token_hex(32)


class SessionRepository:
    def save(self, user_id: int, token: str) -> None:
        print(f"[DB] Сессия сохранена: user_id={user_id}, token={token[:8]}...")


class AuthService:
    def __init__(
        self,
        hasher: PasswordHasher,
        token_generator: TokenGenerator,
        session_repository: SessionRepository,
    ):
        self.hasher = hasher
        self.token_generator = token_generator
        self.session_repository = session_repository

    def authenticate(self, user_id: int, plain: str, hashed: str) -> str | None:
        if not self.hasher.check_password(plain, hashed):
            return None

        token = self.token_generator.generate()
        self.session_repository.save(user_id, token)
        return token


if __name__ == "__main__":
    hasher = PasswordHasher()
    auth_service = AuthService(hasher, TokenGenerator(), SessionRepository())

    stored_hash = hasher.hash_password("secret")
    token = auth_service.authenticate(42, "secret", stored_hash)

    if token is not None:
        print(f"Токен: {token[:8]}...")
