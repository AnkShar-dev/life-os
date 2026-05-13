from life_os.mvp_readiness import readiness_checks


def test_mvp_readiness_finds_missing_controls():
    failures = readiness_checks({"daily_briefing_enabled": False})
    assert "missing_telegram_token" in failures
    assert "missing_approvers" in failures
    assert "daily_briefing_disabled" in failures


def test_mvp_readiness_success():
    failures = readiness_checks(
        {
            "telegram_token": "token-12345",
            "approvers": ["ops"],
            "daily_briefing_enabled": True,
        }
    )
    assert failures == []
