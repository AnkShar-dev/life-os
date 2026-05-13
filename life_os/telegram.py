from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


class TelegramSecurityError(ValueError):
    """Raised when a Telegram operation fails security validation."""


@dataclass(frozen=True)
class TelegramClient:
    """Hardened Telegram sender constraints for MVP safety."""

    allowed_chat_ids: set[str]
    token: str

    def __init__(self, allowed_chat_ids: Iterable[str], token: str) -> None:
        if not token or len(token) < 8:
            raise TelegramSecurityError("Token is missing or malformed")
        clean_ids = {str(chat_id).strip() for chat_id in allowed_chat_ids if str(chat_id).strip()}
        if not clean_ids:
            raise TelegramSecurityError("At least one allowlisted chat ID is required")
        object.__setattr__(self, "allowed_chat_ids", clean_ids)
        object.__setattr__(self, "token", token)

    def validate_destination(self, chat_id: str) -> None:
        if str(chat_id).strip() not in self.allowed_chat_ids:
            raise TelegramSecurityError(f"Blocked non-allowlisted chat_id={chat_id}")
