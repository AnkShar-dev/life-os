from life_os.daily_briefing import DailyBriefingFormatter
from life_os.workflows import ApprovalWorkflow, MarketNewsWorldWorkflow
from life_os.telegram import TelegramClient, TelegramSecurityError


def run_demo() -> str:
    workflow = ApprovalWorkflow(required_approvers={"ops", "owner"})
    workflow.request("deploy-daily-briefing")
    workflow.approve("deploy-daily-briefing", "ops")
    workflow.approve("deploy-daily-briefing", "owner")

    formatter = DailyBriefingFormatter()
    content = formatter.format(
        market={"summary": "Futures are mixed.", "risk_level": "medium"},
        news={"summary": "Top headlines reviewed.", "sources": 5},
        world={"summary": "FX and macro unchanged."},
        approvals=workflow.status("deploy-daily-briefing"),
    )

    client = TelegramClient(allowed_chat_ids={"123"}, token="demo-token")
    client.validate_destination("123")
    return content


if __name__ == "__main__":
    try:
        print(run_demo())
    except TelegramSecurityError as exc:
        print(f"Telegram validation failed: {exc}")
