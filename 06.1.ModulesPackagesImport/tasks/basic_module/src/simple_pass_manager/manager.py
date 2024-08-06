import hashlib
from simple_pass_manager.utils.encryption import password_decrypt, password_encrypt
from simple_pass_manager.utils.generation import generate_urlsafe_password
from simple_pass_manager.exceptions import PasswordLengthError, PasswordNotStoredError

PASS_LEN_MIN = 4


class PasswordManager:
    def __init__(self, secret_password: str, default_pass_len: int = 32):
        assert len(secret_password) > 0
        self._secret_hash = self._hash(secret_password)
        self._secret_storage: dict[str, bytes] = {}

        if default_pass_len < PASS_LEN_MIN:
            raise PasswordLengthError(f'Password length should be >= {PASS_LEN_MIN}')
        self._default_pass_len = default_pass_len

    @staticmethod
    def _hash(obj: str | bytes) -> str:
        if isinstance(obj, str):
            obj = obj.encode()

        return hashlib.sha256(obj).hexdigest()

    def __len__(self) -> int:
        return len(self._secret_storage)

    def validate_secret_hash(self, secret_password: str) -> bool:
        return self._secret_hash == self._hash(secret_password)

    def add_password(self, password: str, name: str) -> None:
        self._secret_storage[name] = password_encrypt(password.encode(), self._secret_hash)

    def get_password(self, name: str) -> str:
        if name not in self._secret_storage:
            raise PasswordNotStoredError(f'{name} is not stored')

        return password_decrypt(self._secret_storage[name], self._secret_hash).decode()

    def generate_password(self, pass_len: int | None = None) -> str:
        pass_len = pass_len or self._default_pass_len
        if pass_len < PASS_LEN_MIN:
            raise PasswordLengthError(f'Password length should be >= {PASS_LEN_MIN}')

        return generate_urlsafe_password(pass_len)


__all__ = ['PasswordManager']
