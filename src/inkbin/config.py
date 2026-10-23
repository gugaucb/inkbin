from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_ENV: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str = "insecure-dev-secret-key-32-chars-long"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    BASE_URL: str = "http://localhost:8000"

    DATABASE_URL: str = "sqlite+aiosqlite:///./inkbin.db"
    REDIS_URL: str | None = None

    RATE_LIMIT_PER_MINUTE: int = 100
    MAX_PASTE_BYTES: int = 1_048_576  # 1 MB

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
