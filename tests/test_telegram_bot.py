import pytest
from unittest.mock import AsyncMock, patch

from jarvis.bot.telegram_bot import TelegramBot, TelegramSecurityError, handle_command, handle_unsupported_command, run_bot, whoami_command


def test_telegram_hardening_allowlist_enforced():
    bot = TelegramBot(token="token-12345", allowed_chat_ids={"123"})
    bot.validate_destination("123")
    with pytest.raises(TelegramSecurityError):
        bot.validate_destination("999")


def test_telegram_hardening_rejects_bad_token():
    with pytest.raises(TelegramSecurityError):
        TelegramBot(token="short", allowed_chat_ids={"123"})


def test_telegram_hardening_empty_allowlist_allows_any_chat():
    bot = TelegramBot(token="token-12345", allowed_chat_ids=set())
    assert bot.validate_destination("123")
    assert bot.validate_destination("999")


def test_telegram_hardening_allowlist_is_immutable_frozenset():
    original = {"123", "456"}
    bot = TelegramBot(token="token-12345", allowed_chat_ids=original)

    original.add("789")

    assert bot.allowed_chat_ids == frozenset({"123", "456"})
    with pytest.raises(AttributeError):
        bot.allowed_chat_ids.add("000")


def test_whoami_command_returns_chat_id():
    reply_text = AsyncMock()
    update = type(
        "UpdateStub",
        (),
        {"effective_chat": type("Chat", (), {"id": 42})(), "message": type("Msg", (), {"reply_text": reply_text})()},
    )()
    context = type("ContextStub", (), {})()

    import asyncio
    asyncio.run(whoami_command(update, context))

    reply_text.assert_awaited_once_with("42")


def test_handle_command_rejects_non_allowlisted_chat():
    reply_text = AsyncMock()
    update = type(
        "UpdateStub",
        (),
        {
            "effective_chat": type("Chat", (), {"id": 999})(),
            "message": type("Msg", (), {"text": "/news", "reply_text": reply_text})(),
        },
    )()
    context = type(
        "ContextStub",
        (),
        {"application": type("App", (), {"bot_data": {"security": TelegramBot(token="token-12345", allowed_chat_ids={"123"})}})()},
    )()

    import asyncio
    with patch("jarvis.bot.telegram_bot.router.route", new=AsyncMock()) as route_mock:
        asyncio.run(handle_command(update, context))
    reply_text.assert_awaited_once_with("Unauthorized chat id.")
    route_mock.assert_not_awaited()


def test_unsupported_command_handler_replies_with_friendly_error():
    reply_text = AsyncMock()
    update = type("UpdateStub", (), {"message": type("Msg", (), {"reply_text": reply_text})()})()
    context = type("ContextStub", (), {})()

    import asyncio
    asyncio.run(handle_unsupported_command(update, context))

    reply_text.assert_awaited_once()


def test_run_bot_rejects_missing_token():
    import asyncio
    with patch("jarvis.bot.telegram_bot.get_settings") as settings_mock:
        settings_mock.return_value = type("S", (), {"telegram_bot_token": "", "allowed_telegram_chat_ids": []})()
        with pytest.raises(TelegramSecurityError):
            asyncio.run(run_bot())
