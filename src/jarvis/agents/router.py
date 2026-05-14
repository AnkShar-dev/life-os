"""Router agent dispatching commands to specialist agents."""

from __future__ import annotations

from jarvis.agents.base import BaseAgent
from jarvis.schemas.common import AgentRequest, AgentResponse


class RouterAgent:
    """Routes command requests to the appropriate specialist."""

    def __init__(self, agents: list[BaseAgent]) -> None:
        self._agents = agents

    async def route(self, request: AgentRequest) -> AgentResponse:
        for agent in self._agents:
            if agent.can_handle(request.command):
                return await agent.handle(request)
        return AgentResponse(agent="router", summary=f"Unsupported command: {request.command}")
