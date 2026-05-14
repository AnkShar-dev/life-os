from jarvis.workflows.daily_briefing_formatter import DailyBriefingFormatter


def test_daily_briefing_formatter_includes_approval_summary():
    output = DailyBriefingFormatter().format(
        summary="Core updates complete.",
        approvals={"approved": True, "approved_by": ["ops"]},
    )

    assert "# Daily Briefing" in output
    assert "✅ Approved" in output
    assert "## Summary" in output
