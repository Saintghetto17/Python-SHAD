import secrets

from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

BACKEND = default_backend()

ITERATIONS = 100_000


def password_encrypt(message: bytes, password: str, iterations: int = ITERATIONS) -> bytes:
    """Encrypt message using password to generate key"""
    salt = secrets.token_bytes(16)
    key = _derive_key(password.encode(), salt, iterations)
    return b64e(
        b'%b%b%b' % (
            salt,
            iterations.to_bytes(4, 'big'),
            b64d(Fernet(key).encrypt(message)),
        )
    )


def password_decrypt(token: bytes, password: str) -> bytes:
    """Decrypt message from token using password to generate key"""
    decoded = b64d(token)
    salt, iter, token = decoded[:16], decoded[16:20], b64e(decoded[20:])
    iterations = int.from_bytes(iter, 'big')
    key = _derive_key(password.encode(), salt, iterations)
    return Fernet(key).decrypt(token)


def _derive_key(password: bytes, salt: bytes, iterations: int = ITERATIONS) -> bytes:
    """Derive a secret key from a given password and salt"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(), length=32, salt=salt,
        iterations=iterations, backend=BACKEND)
    return b64e(kdf.derive(password))


def generate_key() -> bytes:
    """Generate key for encryption"""
    return Fernet.generate_key()


def key_encrypt(message: bytes, key: bytes) -> bytes:
    """Encrypt message using secret key"""
    return Fernet(key).encrypt(message)


def key_decrypt(token: bytes, key: bytes) -> bytes:
    """Decrypt message from token using secret key"""
    return Fernet(key).decrypt(token)


__all__ = ['password_encrypt', 'password_decrypt', 'key_encrypt', 'key_decrypt', 'generate_key']
