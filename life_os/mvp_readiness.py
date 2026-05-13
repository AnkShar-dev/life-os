from __future__ import annotations


def readiness_checks(config: dict) -> list[str]:
    """Minimal MVP readiness checks used before deploys."""
    failures: list[str] = []
    if not config.get("telegram_token"):
        failures.append("missing_telegram_token")
    if not config.get("approvers"):
        failures.append("missing_approvers")
    if config.get("daily_briefing_enabled") is not True:
        failures.append("daily_briefing_disabled")
    return failures
