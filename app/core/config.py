from functools import lru_cache
from typing import Literal

from pydantic import AnyHttpUrl, Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_depth=2,  # ty: ignore
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "VAMpy"
    app_version: str = "0.0.1"
    debug: bool = False
    environment: Literal["dev", "prod"] = "prod"

    api_v1_prefix: str = "/api/v1"

    postgres_user: str
    postgres_password: str
    postgres_host: str = "127.0.0.1"
    postgres_port: int = 5432
    postgres_db: str

    db_pool_size: int = 5
    db_max_overflow: int = 10
    db_pool_timeout: int = 30
    db_pool_recycle: int = 1800
    db_echo: bool = False

    @computed_field
    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    secret_key: str = Field(..., min_length=32)  # It's also used as JWT secret key
    algorithm: str = "HS256"  # jwt algorithm
    leeway_seconds: int = 10
    access_token_minutes: int = 15
    refresh_token_days: int = 15

    allowed_hosts: list[AnyHttpUrl] = []

    @computed_field
    @property
    def is_production(self) -> bool:
        return self.environment == "prod"


@lru_cache
def get_settings() -> Settings:
    return Settings()
