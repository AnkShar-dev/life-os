from __future__ import annotations


class DailyBriefingFormatter:
    """Formats a concise daily briefing with approvals."""

    def format(self, market: dict, news: dict, world: dict, approvals: dict) -> str:
        approved_flag = "✅ Approved" if approvals.get("approved") else "⏳ Pending Approval"
        return (
            "# Daily Briefing\n\n"
            f"Approval: {approved_flag}\n"
            f"Approvers: {', '.join(approvals.get('approved_by', [])) or 'none'}\n\n"
            "## Market\n"
            f"- Summary: {market.get('summary', 'n/a')}\n"
            f"- Risk: {market.get('risk_level', 'n/a')}\n\n"
            "## News\n"
            f"- Summary: {news.get('summary', 'n/a')}\n"
            f"- Sources Reviewed: {news.get('sources', 'n/a')}\n\n"
            "## World\n"
            f"- Summary: {world.get('summary', 'n/a')}\n"
        )
