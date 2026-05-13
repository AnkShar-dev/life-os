from life_os.workflows import ApprovalError, ApprovalWorkflow, MarketNewsWorldWorkflow


def test_end_to_end_approval_workflow():
    wf = ApprovalWorkflow(required_approvers={"ops", "owner"})
    wf.request("job1")
    wf.approve("job1", "ops")
    assert wf.status("job1")["approved"] is False
    wf.approve("job1", "owner")
    status = wf.status("job1")
    assert status["approved"] is True
    assert status["approved_by"] == ["ops", "owner"]


def test_unexpected_approver_rejected():
    wf = ApprovalWorkflow(required_approvers={"ops"})
    wf.request("job2")
    try:
        wf.approve("job2", "intruder")
    except ApprovalError as exc:
        assert "Unexpected approver" in str(exc)
    else:
        raise AssertionError("approval should have failed")


def test_market_news_world_workflow_refactor_contract():
    result = MarketNewsWorldWorkflow().run({"a": 1}, {"b": 2}, {"c": 3})
    assert result["status"] == "ready"
    assert result["sections"] == ["market", "news", "world"]
