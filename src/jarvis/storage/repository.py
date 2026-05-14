from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class PendingApproval:
    request_id: str
    required_approvers: set[str]
    approved_by: set[str] = field(default_factory=set)


class ApprovalRepository:
    """In-memory pending approval store/listing for workflow orchestration."""

    def __init__(self) -> None:
        self._pending: dict[str, PendingApproval] = {}

    def save(self, request: PendingApproval) -> None:
        self._pending[request.request_id] = request

    def get(self, request_id: str) -> PendingApproval | None:
        return self._pending.get(request_id)

    def list_pending(self) -> list[PendingApproval]:
        return sorted(self._pending.values(), key=lambda item: item.request_id)
