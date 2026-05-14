import pytest

from jarvis.services.approval import ApprovalError, ApprovalService
from jarvis.storage.repository import ApprovalRepository


def test_end_to_end_approval_flow():
    repo = ApprovalRepository()
    service = ApprovalService(required_approvers={"ops", "owner"}, repository=repo)

    service.request("briefing-1")
    service.approve("briefing-1", "ops")
    assert service.status("briefing-1")["approved"] is False

    service.approve("briefing-1", "owner")
    status = service.status("briefing-1")
    assert status["approved"] is True
    assert status["approved_by"] == ["ops", "owner"]


def test_approval_pending_listing_storage():
    repo = ApprovalRepository()
    service = ApprovalService(required_approvers={"ops"}, repository=repo)

    service.request("b")
    service.request("a")
    pending = repo.list_pending()
    assert [item.request_id for item in pending] == ["a", "b"]


def test_unexpected_approver_rejected():
    repo = ApprovalRepository()
    service = ApprovalService(required_approvers={"ops"}, repository=repo)
    service.request("briefing-2")

    with pytest.raises(ApprovalError):
        service.approve("briefing-2", "intruder")
