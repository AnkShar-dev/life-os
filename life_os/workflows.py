from __future__ import annotations

from dataclasses import dataclass, field


class ApprovalError(RuntimeError):
    pass


@dataclass
class ApprovalRequest:
    request_id: str
    required_approvers: set[str]
    approved_by: set[str] = field(default_factory=set)

    @property
    def approved(self) -> bool:
        return self.required_approvers.issubset(self.approved_by)


class ApprovalWorkflow:
    """Simple end-to-end approval state machine."""

    def __init__(self, required_approvers: set[str]) -> None:
        if not required_approvers:
            raise ApprovalError("required_approvers cannot be empty")
        self.required_approvers = required_approvers
        self._requests: dict[str, ApprovalRequest] = {}

    def request(self, request_id: str) -> None:
        self._requests[request_id] = ApprovalRequest(request_id, set(self.required_approvers))

    def approve(self, request_id: str, approver: str) -> None:
        if approver not in self.required_approvers:
            raise ApprovalError(f"Unexpected approver: {approver}")
        req = self._requests.get(request_id)
        if not req:
            raise ApprovalError(f"Unknown request_id: {request_id}")
        req.approved_by.add(approver)

    def status(self, request_id: str) -> dict[str, object]:
        req = self._requests.get(request_id)
        if not req:
            raise ApprovalError(f"Unknown request_id: {request_id}")
        return {
            "request_id": req.request_id,
            "approved": req.approved,
            "approved_by": sorted(req.approved_by),
            "required_approvers": sorted(req.required_approvers),
        }


class MarketNewsWorldWorkflow:
    """Refactored unified market/news/world workflow."""

    def run(self, market: dict, news: dict, world: dict) -> dict:
        return {
            "market": market,
            "news": news,
            "world": world,
            "status": "ready",
            "sections": ["market", "news", "world"],
        }
