"""Approval workflow service."""

from __future__ import annotations

import uuid

from jarvis.schemas.common import ApprovalDecision, ApprovalRequest
from jarvis.storage.repository import ApprovalRepository, SQLiteRepository


class ApprovalError(ValueError):
    """Raised for invalid approval actions."""


class ApprovalService:
    """Creates and resolves approval requests for risky actions."""

    def __init__(self, repository: SQLiteRepository | ApprovalRepository, required_approvers: set[str] | None = None) -> None:
        self.repository = repository
        self.required_approvers = required_approvers or set()

    def create(self, action_type: str, payload: dict) -> ApprovalRequest:
        approval = ApprovalRequest(approval_id=str(uuid.uuid4()), action_type=action_type, payload=payload)
        if hasattr(self.repository, "save_approval"):
            self.repository.save_approval(approval.approval_id, action_type, payload)
        return approval

    def decide(self, decision: ApprovalDecision) -> str:
        status = "approved" if decision.decision.lower() == "approve" else "rejected"
        if hasattr(self.repository, "set_approval_status"):
            self.repository.set_approval_status(decision.approval_id, status)
        return status

    def request(self, request_id: str) -> None:
        if not isinstance(self.repository, ApprovalRepository):
            raise ApprovalError("request is only supported with ApprovalRepository")
        self.repository.request(request_id)

    def approve(self, request_id: str, approver: str) -> None:
        if not isinstance(self.repository, ApprovalRepository):
            raise ApprovalError("approve is only supported with ApprovalRepository")
        if approver not in self.required_approvers:
            raise ApprovalError("approver not allowed")
        self.repository.approve(request_id, approver)

    def status(self, request_id: str) -> dict[str, object]:
        if not isinstance(self.repository, ApprovalRepository):
            raise ApprovalError("status is only supported with ApprovalRepository")
        return self.repository.status(request_id, self.required_approvers)
