"""Approval workflow service."""

from __future__ import annotations

import uuid

from jarvis.schemas.common import ApprovalDecision, ApprovalRequest
from jarvis.storage.repository import SQLiteRepository


class ApprovalService:
    """Creates and resolves approval requests for risky actions."""

    def __init__(self, repository: SQLiteRepository) -> None:
        self.repository = repository

    def create(self, action_type: str, payload: dict) -> ApprovalRequest:
        approval = ApprovalRequest(approval_id=str(uuid.uuid4()), action_type=action_type, payload=payload)
        self.repository.save_approval(approval.approval_id, action_type, payload)
        return approval

    def decide(self, decision: ApprovalDecision) -> str:
        status = "approved" if decision.decision.lower() == "approve" else "rejected"
        self.repository.set_approval_status(decision.approval_id, status)
        return status
