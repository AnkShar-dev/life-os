from jarvis.core.config import get_settings


def test_allowed_telegram_chat_ids_parsing(monkeypatch):
    get_settings.cache_clear()
    monkeypatch.setenv("APP_ALLOWED_TELEGRAM_CHAT_IDS", "123,456")

    settings = get_settings()

    assert settings.allowed_telegram_chat_ids == ["123", "456"]
    get_settings.cache_clear()
