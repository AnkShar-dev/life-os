from life_os.daily_briefing import DailyBriefingFormatter


def test_daily_briefing_formatter_includes_approval_and_sections():
    out = DailyBriefingFormatter().format(
        market={"summary": "Stable", "risk_level": "low"},
        news={"summary": "Light day", "sources": 3},
        world={"summary": "Calm"},
        approvals={"approved": True, "approved_by": ["ops"]},
    )
    assert "# Daily Briefing" in out
    assert "✅ Approved" in out
    assert "## Market" in out and "## News" in out and "## World" in out
