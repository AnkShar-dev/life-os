import pytest

from life_os.telegram import TelegramClient, TelegramSecurityError


def test_telegram_hardening_allowlist_enforced():
    client = TelegramClient(allowed_chat_ids={"123"}, token="token-12345")
    client.validate_destination("123")
    with pytest.raises(TelegramSecurityError):
        client.validate_destination("999")


def test_telegram_hardening_rejects_bad_token():
    with pytest.raises(TelegramSecurityError):
        TelegramClient(allowed_chat_ids={"1"}, token="short")
