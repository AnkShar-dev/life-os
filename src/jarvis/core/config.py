"""Application configuration."""

from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Global settings loaded from environment."""

    model_config = SettingsConfigDict(env_prefix="APP_", env_file=".env", extra="ignore")

    env: str = "local"
    log_level: str = "INFO"
    storage_backend: Literal["sqlite", "sheets", "postgres"] = "sqlite"
    sqlite_path: str = "./data/jarvis.db"
    telegram_bot_token: str = ""
    news_sources: list[str] = Field(default_factory=list)
    market_sources: list[str] = Field(default_factory=list)
    enable_mock_data: bool = True


@lru_cache
def get_settings() -> Settings:
    """Return cached settings instance."""

    return Settings()
