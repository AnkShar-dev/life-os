"""Base abstractions for all agents."""

from abc import ABC, abstractmethod

from jarvis.schemas.common import AgentRequest, AgentResponse


class BaseAgent(ABC):
    """Common interface each specialist agent implements."""

    name: str
    supported_commands: set[str]

    @abstractmethod
    async def handle(self, request: AgentRequest) -> AgentResponse:
        """Handle an incoming request."""

    def can_handle(self, command: str) -> bool:
        """Return True if this agent can process the command."""

        return command in self.supported_commands
