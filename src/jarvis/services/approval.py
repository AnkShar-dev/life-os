from __future__ import annotations

from jarvis.storage.repository import ApprovalRepository, PendingApproval


class ApprovalError(RuntimeError):
    pass


class ApprovalService:
    """End-to-end approval flow backed by ApprovalRepository."""

    def __init__(self, required_approvers: set[str], repository: ApprovalRepository) -> None:
        if not required_approvers:
            raise ApprovalError("required_approvers cannot be empty")
        self.required_approvers = set(required_approvers)
        self.repository = repository

    def request(self, request_id: str) -> None:
        self.repository.save(PendingApproval(request_id=request_id, required_approvers=set(self.required_approvers)))

    def approve(self, request_id: str, approver: str) -> None:
        if approver not in self.required_approvers:
            raise ApprovalError(f"Unexpected approver: {approver}")
        request = self.repository.get(request_id)
        if not request:
            raise ApprovalError(f"Unknown request_id: {request_id}")
        request.approved_by.add(approver)

    def status(self, request_id: str) -> dict[str, object]:
        request = self.repository.get(request_id)
        if not request:
            raise ApprovalError(f"Unknown request_id: {request_id}")

        approved = request.required_approvers.issubset(request.approved_by)
        return {
            "request_id": request.request_id,
            "approved": approved,
            "approved_by": sorted(request.approved_by),
            "required_approvers": sorted(request.required_approvers),
        }
