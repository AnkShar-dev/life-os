from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


class TelegramSecurityError(ValueError):
    """Raised when Telegram destination/token validation fails."""


@dataclass(frozen=True)
class TelegramBot:
    """Hardened Telegram sender with explicit allowlist constraints."""

    token: str
    allowed_chat_ids: set[str]

    def __init__(self, token: str, allowed_chat_ids: Iterable[str]) -> None:
        token = (token or "").strip()
        if len(token) < 8:
            raise TelegramSecurityError("Token is missing or malformed")

        clean_ids = {str(chat_id).strip() for chat_id in allowed_chat_ids if str(chat_id).strip()}
        if not clean_ids:
            raise TelegramSecurityError("At least one allowlisted chat ID is required")

        object.__setattr__(self, "token", token)
        object.__setattr__(self, "allowed_chat_ids", clean_ids)

    def validate_destination(self, chat_id: str) -> None:
        if str(chat_id).strip() not in self.allowed_chat_ids:
            raise TelegramSecurityError(f"Blocked non-allowlisted chat_id={chat_id}")
