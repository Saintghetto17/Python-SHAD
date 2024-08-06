import pytest
from cryptography.fernet import InvalidToken

from simple_pass_manager.utils.encryption import password_decrypt, password_encrypt, \
    generate_key, key_decrypt, key_encrypt


class TestKey:
    def test_key_generation(self) -> None:
        key = generate_key()
        assert isinstance(key, bytes)
        assert 0 < len(key) < 128

    @pytest.mark.parametrize('message', [
        '',
        'a',
        '123',
        '@($#NDASK()(!@SDAK as ASDJ)@JKLDSA)@++',
        '😀 Grinning Face 😵‍💫 Face with Spiral Eyes',
        '128' * 128,
    ])
    def test_encrypt_decrypt(self, message: str) -> None:
        message_bytes = message.encode()
        key = generate_key()

        encrypted_message = key_encrypt(message_bytes, key)
        assert encrypted_message != message_bytes

        wrong_key = generate_key()
        with pytest.raises(InvalidToken):
            key_decrypt(encrypted_message, wrong_key).decode()

        decrypted_message = key_decrypt(encrypted_message, key).decode()
        assert decrypted_message == message


class TestPassword:
    @pytest.mark.parametrize('message', [
        '',
        'a',
        '123',
        '@($#NDASK()(!@SDAK as ASDJ)@JKLDSA)@++',
        '😀 Grinning Face 😵‍💫 Face with Spiral Eyes',
        '128' * 128,
    ])
    @pytest.mark.parametrize('password', [
        'password',
        '64' * 16,
    ])
    def test_encrypt_decrypt(self, message: str, password: str) -> None:
        message_bytes = message.encode()

        encrypted_message = password_encrypt(message_bytes, password)
        assert encrypted_message != message_bytes

        wrong_password = 'wrong_password'
        with pytest.raises(InvalidToken):
            password_decrypt(encrypted_message, wrong_password).decode()

        decrypted_message = password_decrypt(encrypted_message, password).decode()
        assert decrypted_message == message
