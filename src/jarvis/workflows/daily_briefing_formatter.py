from __future__ import annotations


class DailyBriefingFormatter:
    """Formats briefing payload with approval status."""

    def format(self, summary: str, approvals: dict[str, object]) -> str:
        approved_flag = "✅ Approved" if approvals.get("approved") else "⏳ Pending Approval"
        approvers = approvals.get("approved_by") or []
        approvers_text = ", ".join(approvers) if approvers else "none"
        return "\n".join([
            "# Daily Briefing",
            "",
            f"Approval: {approved_flag}",
            f"Approvers: {approvers_text}",
            "",
            "## Summary",
            f"- {summary}",
        ])
