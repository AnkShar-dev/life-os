"""Telegram bot entrypoint for Jarvis."""

from __future__ import annotations

from dataclasses import dataclass

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

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
        object.__setattr__(self, "token", token)
        object.__setattr__(self, "allowed_chat_ids", frozenset(allowed_chat_ids))

    def validate_destination(self, chat_id: str) -> bool:
        if self.allowed_chat_ids and chat_id not in self.allowed_chat_ids:
            raise TelegramSecurityError(f"Chat id {chat_id} is not in allowlist.")
        return True


async def whoami_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    del context
    if update.effective_chat is None or update.message is None:
        return
    await update.message.reply_text(str(update.effective_chat.id))


async def handle_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    bot: TelegramBot = context.application.bot_data["security"]
    chat_id = str(update.effective_chat.id) if update.effective_chat is not None else ""
    try:
        bot.validate_destination(chat_id)
    except TelegramSecurityError:
        if update.message is not None:
            await update.message.reply_text("Unauthorized chat id.")
        return

    if update.message is None or update.message.text is None:
        return
    cmd = update.message.text.split()[0]
    request = AgentRequest(command=cmd)
    response = await router.route(request)
    if response.agent == "router":
        await update.message.reply_text("Sorry, I don't support that command yet. Try /news, /market, /world, /brief, or /whoami.")
        return
    await update.message.reply_text(f"{response.summary}\n{response.details}")


async def handle_unsupported_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    del context
    if update.message is None:
        return
    await update.message.reply_text("Sorry, I don't support that command yet. Try /news, /market, /world, /brief, or /whoami.")


async def run_bot() -> None:
    settings = get_settings()
    if not settings.telegram_bot_token:
        raise TelegramSecurityError("Missing APP_TELEGRAM_BOT_TOKEN. Add it in your .env before starting Telegram bot.")
    security = TelegramBot(
        token=settings.telegram_bot_token,
        allowed_chat_ids={chat_id.strip() for chat_id in settings.allowed_telegram_chat_ids if chat_id.strip()},
    )
    app = Application.builder().token(security.token).build()
    app.bot_data["security"] = security

    for command in ["news", "market", "world", "brief", "finance", "resume", "jobs", "reel", "trade"]:
        app.add_handler(CommandHandler(command, handle_command))
    app.add_handler(CommandHandler("whoami", whoami_command))

    app.add_handler(CommandHandler("approve", handle_command))
    app.add_handler(CommandHandler("reject", handle_command))
    app.add_handler(MessageHandler(filters.COMMAND, handle_unsupported_command))

    await app.initialize()
    await app.start()
    await app.updater.start_polling()
