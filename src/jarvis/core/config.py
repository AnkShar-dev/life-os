"""Application configuration."""

from functools import lru_cache
from typing import Annotated, Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


class Settings(BaseSettings):
    """Global settings loaded from environment."""

    model_config = SettingsConfigDict(env_prefix="APP_", env_file=".env", extra="ignore")

    env: str = "local"
    log_level: str = "INFO"
    storage_backend: Literal["sqlite", "sheets", "postgres"] = "sqlite"
    sqlite_path: str = "./data/jarvis.db"
    telegram_bot_token: str = ""
    allowed_telegram_chat_ids: Annotated[list[str], NoDecode] = Field(default_factory=list)
    news_sources: list[str] = Field(default_factory=list)
    market_sources: list[str] = Field(default_factory=list)
    world_sources: list[str] = Field(default_factory=list)
    enable_mock_data: bool = True

    @field_validator("allowed_telegram_chat_ids", mode="before")
    @classmethod
    def _parse_allowed_chat_ids(cls, value: object) -> object:
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value


@lru_cache
def get_settings() -> Settings:
    """Return cached settings instance."""

    return Settings()
