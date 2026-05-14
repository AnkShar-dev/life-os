import pytest

from jarvis.bot.telegram_bot import TelegramBot, TelegramSecurityError


def test_telegram_hardening_allowlist_enforced():
    bot = TelegramBot(token="token-12345", allowed_chat_ids={"123"})
    bot.validate_destination("123")
    with pytest.raises(TelegramSecurityError):
        bot.validate_destination("999")


def test_telegram_hardening_rejects_bad_token():
    with pytest.raises(TelegramSecurityError):
        TelegramBot(token="short", allowed_chat_ids={"123"})
