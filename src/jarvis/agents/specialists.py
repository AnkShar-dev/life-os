"""Specialist agent implementations for Jarvis MVP."""

from __future__ import annotations

from jarvis.agents.base import BaseAgent
from jarvis.schemas.common import AgentRequest, AgentResponse
from jarvis.services.approval import ApprovalService
from jarvis.storage.repository import SQLiteRepository


class NewsAgent(BaseAgent):
    name = "news"
    supported_commands = {"/news"}

    async def handle(self, request: AgentRequest) -> AgentResponse:
        return AgentResponse(
            agent=self.name,
            summary="Top AI/tech stories prepared.",
            details={"brief": ["AI infra costs are falling.", "New agentic tools shipping fast."], "why_it_matters": "Faster iteration and lower build cost."},
        )


class MarketAgent(BaseAgent):
    name = "market"
    supported_commands = {"/market"}

    async def handle(self, request: AgentRequest) -> AgentResponse:
        return AgentResponse(agent=self.name, summary="Daily market update prepared.", details={"note": "No trades executed."})


class TradingAgent(BaseAgent):
    name = "trading"
    supported_commands = {"/trade"}

    def __init__(self, approvals: ApprovalService, repo: SQLiteRepository) -> None:
        self.approvals = approvals
        self.repo = repo

    async def handle(self, request: AgentRequest) -> AgentResponse:
        idea = {"symbol": "NVDA", "setup": "pullback", "risk_pct": 1}
        self.repo.log_trade(idea)
        approval = self.approvals.create("trade_execution", idea)
        return AgentResponse(agent=self.name, summary="Trade idea generated; awaiting approval.", details={"idea": idea, "approval_id": approval.approval_id})


class FinanceAgent(BaseAgent):
    name = "finance"
    supported_commands = {"/finance"}

    async def handle(self, request: AgentRequest) -> AgentResponse:
        return AgentResponse(agent=self.name, summary="Weekly finance snapshot ready.", details={"suggestion": "Reduce discretionary spend by 10%."})


class ResumeAgent(BaseAgent):
    name = "resume"
    supported_commands = {"/resume"}

    def __init__(self, repo: SQLiteRepository) -> None:
        self.repo = repo

    async def handle(self, request: AgentRequest) -> AgentResponse:
        tailored = {"role": request.payload.get("role", "Software Engineer"), "format": "ATS-friendly"}
        self.repo.save_resume_version(tailored)
        return AgentResponse(agent=self.name, summary="Resume tailored and versioned.", details=tailored)


class JobAgent(BaseAgent):
    name = "jobs"
    supported_commands = {"/jobs"}

    def __init__(self, approvals: ApprovalService) -> None:
        self.approvals = approvals

    async def handle(self, request: AgentRequest) -> AgentResponse:
        draft = {"company": "ExampleAI", "role": "Applied AI Engineer", "score": 86}
        approval = self.approvals.create("job_apply", draft)
        return AgentResponse(agent=self.name, summary="Job matches and draft application prepared.", details={"job": draft, "approval_id": approval.approval_id})


class InstagramAgent(BaseAgent):
    name = "instagram"
    supported_commands = {"/reel"}

    def __init__(self, approvals: ApprovalService) -> None:
        self.approvals = approvals

    async def handle(self, request: AgentRequest) -> AgentResponse:
        post = {"hook": "3 AI tools I use daily", "caption": "My quick stack for faster execution.", "hashtags": ["#ai", "#productivity"]}
        approval = self.approvals.create("instagram_post", post)
        return AgentResponse(agent=self.name, summary="Reel concept queued; awaiting approval.", details={"reel": post, "approval_id": approval.approval_id})
