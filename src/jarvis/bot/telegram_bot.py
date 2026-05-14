"""Telegram bot entrypoint for Jarvis."""

from __future__ import annotations

from dataclasses import dataclass

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from jarvis.api.main import router
from jarvis.core.config import get_settings
from jarvis.schemas.common import AgentRequest


class TelegramSecurityError(ValueError):
    """Raised when bot hardening checks fail."""


@dataclass(frozen=True, slots=True)
class TelegramBot:
    token: str
    allowed_chat_ids: frozenset[str]

    def __init__(self, token: str, allowed_chat_ids: set[str] | frozenset[str]) -> None:
        if len(token) < 10:
            raise TelegramSecurityError("Telegram bot token appears invalid.")
        if not allowed_chat_ids:
            raise TelegramSecurityError("At least one allowed chat id is required.")
        object.__setattr__(self, "token", token)
        object.__setattr__(self, "allowed_chat_ids", frozenset(allowed_chat_ids))

    def validate_destination(self, chat_id: str) -> None:
        if chat_id not in self.allowed_chat_ids:
            raise TelegramSecurityError(f"Chat id {chat_id} is not in allowlist.")


async def handle_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None or update.message.text is None:
        return
    cmd = update.message.text.split()[0]
    request = AgentRequest(command=cmd)
    response = await router.route(request)
    await update.message.reply_text(f"{response.summary}\n{response.details}")


async def run_bot() -> None:
    settings = get_settings()
    app = Application.builder().token(settings.telegram_bot_token).build()

    for command in ["news", "market", "world", "brief", "finance", "resume", "jobs", "reel", "trade"]:
        app.add_handler(CommandHandler(command, handle_command))

    app.add_handler(CommandHandler("approve", handle_command))
    app.add_handler(CommandHandler("reject", handle_command))

    await app.initialize()
    await app.start()
    await app.updater.start_polling()
