class PasswordManagerError(ValueError):
    pass


class PasswordNotStoredError(PasswordManagerError):
    pass


class PasswordLengthError(PasswordManagerError):
    pass


__all__ = ['PasswordManagerError', 'PasswordNotStoredError', 'PasswordLengthError']
