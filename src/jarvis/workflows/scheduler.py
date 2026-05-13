"""Scheduler hook stubs for cron/n8n integration."""

from jarvis.schemas.common import AgentRequest


def build_daily_workflows() -> list[AgentRequest]:
    """Return daily scheduled tasks for orchestration tools."""

    return [
        AgentRequest(command="/news"),
        AgentRequest(command="/market"),
        AgentRequest(command="/finance"),
    ]
