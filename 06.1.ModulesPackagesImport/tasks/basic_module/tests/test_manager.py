import pytest

from simple_pass_manager.manager import PasswordManager
from simple_pass_manager.exceptions import PasswordLengthError, PasswordNotStoredError


class TestPasswordManager:
    def test_pass_len(self) -> None:
        secret_password = 'secret-password'

        password_manager = PasswordManager(secret_password)
        assert len(password_manager) == 0
        assert len(password_manager.generate_password()) == password_manager._default_pass_len

        password_manager = PasswordManager(secret_password, default_pass_len=16)
        assert len(password_manager) == 0
        assert len(password_manager.generate_password()) == password_manager._default_pass_len == 16

        with pytest.raises(PasswordLengthError):
            PasswordManager(secret_password, default_pass_len=2)

        with pytest.raises(PasswordLengthError):
            password_manager = PasswordManager(secret_password, default_pass_len=16)
            password_manager.generate_password(2)

    @pytest.mark.parametrize('obj', [
        '1234', '', '(@JFA_SK{FASDFPK@P)$(M$F', b'1234', b'', b'JSDFNJ)!N)!FI)!CSL:AD'
    ])
    def test_hash(self, obj: str | bytes) -> None:
        hash_value = PasswordManager._hash(obj)
        assert isinstance(hash_value, str)
        assert len(hash_value) > 0

    def test_adding_password(self) -> None:
        secret_password = 'secret-password'
        password_manager = PasswordManager(secret_password)
        assert len(password_manager) == 0

        password_manager.add_password('new-password', 'new-password')
        assert len(password_manager) == 1

        password_manager.add_password('new-password-2', 'new-password-2')
        assert len(password_manager) == 2

        password_manager.add_password('new-password-1234', 'new-password-2')
        assert len(password_manager) == 2

    def test_get_password(self) -> None:
        secret_password = 'secret-password'
        password_manager = PasswordManager(secret_password)
        assert len(password_manager) == 0

        password_to_add = 'new-password'
        password_manager.add_password(password_to_add, 'pass')
        password_got = password_manager.get_password('pass')
        assert password_got == password_to_add

        with pytest.raises(PasswordNotStoredError):
            password_manager.get_password('wrong-password-name')
