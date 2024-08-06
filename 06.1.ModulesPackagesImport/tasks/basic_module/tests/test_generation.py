import string

import pytest

from simple_pass_manager.utils.generation import generate_urlsafe_password, generate_password


class TestUrlsafeGenerators:
    @pytest.mark.parametrize('pass_len', [1, 10, 16, 32, 128])
    def test_length(self, pass_len: int) -> None:
        password = generate_urlsafe_password(pass_len=pass_len)
        assert len(password) == pass_len


class TestGeneralGenerators:
    @pytest.mark.parametrize('pass_len', [1, 10, 16, 32, 128])
    def test_length(self, pass_len: int) -> None:
        password = generate_password(pass_len=pass_len)
        assert len(password) == pass_len

    def test_parameters(self) -> None:
        password = generate_password(letters=True, digits=False, special=False)
        assert set(password).issubset(set(string.ascii_letters))

        password = generate_password(letters=False, digits=True, special=False)
        assert set(password).issubset(set(string.digits))

        password = generate_password(letters=False, digits=False, special=True)
        assert set(password).issubset(set('-_+#!@$%^:;*()[]'))
