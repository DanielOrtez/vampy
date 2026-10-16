from fastapi import status

from app.core.exceptions import VAMException


class AuthException(VAMException):
    status_code: int = status.HTTP_401_UNAUTHORIZED


class InvalidCredentials(AuthException):
    error: str = "invalid_credentials"
    detail: str = "Invalid credentials."


class InvalidAccessToken(AuthException):
    error: str = "invalid_access_token"
    detail: str = "Invalid access token."


class InvalidRefreshToken(AuthException):
    error: str = "invalid_refresh_token"
    detail: str = "Invalid refresh token."
