from fastapi import status


class AuthException(Exception):
    status_code: int = status.HTTP_401_UNAUTHORIZED


class InvalidCredentials(AuthException):
    message: str = "Invalid credentials."

    def __init__(self):
        super().__init__(self.message)


class InvalidAccessToken(AuthException):
    message: str = "Invalid access token."

    def __init__(self):
        super().__init__(self.message)


class InvalidRefreshToken(AuthException):
    message: str = "Invalid refresh token."

    def __init__(self):
        super().__init__(self.message)
