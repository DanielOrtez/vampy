from fastapi import status


class AuthException(Exception):
    status_code: int = status.HTTP_401_UNAUTHORIZED


class InvalidCredentials(AuthException):
    def __init__(self):
        super().__init__("Invalid credentials.")


class InvalidRefreshToken(AuthException):
    def __init__(self):
        super().__init__("Invalid refresh token.")
