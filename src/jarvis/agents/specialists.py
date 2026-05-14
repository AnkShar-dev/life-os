"""Specialist agent implementations for Jarvis MVP."""

from __future__ import annotations

from jarvis.agents.base import BaseAgent
from jarvis.core.config import Settings, get_settings
from jarvis.schemas.common import AgentRequest, AgentResponse
from jarvis.services.approval import ApprovalService
from jarvis.services.briefing_sources import BriefingSourceService
from jarvis.storage.repository import SQLiteRepository


class NewsAgent(BaseAgent):
    name = "news"
    supported_commands = {"/news"}

    def __init__(self, source_service: BriefingSourceService | None = None, settings: Settings | None = None) -> None:
        self.source_service = source_service or BriefingSourceService()
        self.settings = settings or get_settings()

    async def handle(self, request: AgentRequest) -> AgentResponse:
        fallback = [
            {"title": "Frontier model launches accelerate product cycles.", "source": "mock"},
            {"title": "AI copilots spread across enterprise workflows.", "source": "mock"},
            {"title": "Cloud + chips capex indicates sustained infra race.", "source": "mock"},
        ]
        headlines, used_mock = self.source_service.fetch_or_fallback(self.settings.news_sources, fallback)
        return AgentResponse(
            agent=self.name,
            summary="AI & tech briefing ready.",
            details={
                "headlines": headlines,
                "builder_relevance": "Builder product velocity, tooling choices, and model integration patterns.",
                "investor_relevance": "Revenue capture, infra spend, and competitive moat signals.",
                "why_it_matters": "AI platform shifts can rapidly change both startup execution and listed tech valuations.",
                "source_labels": self.source_service.labels(headlines),
                "fallback_used": used_mock,
            },
        )


class MarketAgent(BaseAgent):
    name = "market"
    supported_commands = {"/market"}

    def __init__(self, source_service: BriefingSourceService | None = None, settings: Settings | None = None) -> None:
        self.source_service = source_service or BriefingSourceService()
        self.settings = settings or get_settings()

    async def handle(self, request: AgentRequest) -> AgentResponse:
        fallback = [
            {"title": "Indian indices trade mixed ahead of policy signals.", "source": "mock"},
            {"title": "Banks and IT lead direction while defensives stabilize.", "source": "mock"},
            {"title": "Foreign flow and crude movement set near-term tone.", "source": "mock"},
        ]
        headlines, used_mock = self.source_service.fetch_or_fallback(self.settings.market_sources, fallback)
        return AgentResponse(
            agent=self.name,
            summary="India market briefing ready.",
            details={
                "indices": ["Nifty 50", "Sensex", "Bank Nifty"],
                "sector_context": ["IT", "Banking", "Auto", "Pharma", "Energy"],
                "macro_context": ["Oil", "INR", "Inflation", "RBI", "FII/DII flows"],
                "headlines": headlines,
                "note": "No trade execution.",
                "fallback_used": used_mock,
            },
        )


class WorldAgent(BaseAgent):
    name = "world"
    supported_commands = {"/world"}

    def __init__(self, source_service: BriefingSourceService | None = None, settings: Settings | None = None) -> None:
        self.source_service = source_service or BriefingSourceService()
        self.settings = settings or get_settings()

    async def handle(self, request: AgentRequest) -> AgentResponse:
        fallback = [
            {"title": "US rates path and inflation prints remain key risk drivers.", "source": "mock"},
            {"title": "Oil volatility and shipping risk shape energy outlook.", "source": "mock"},
            {"title": "Tech regulation and AI policy tighten globally.", "source": "mock"},
        ]
        headlines, used_mock = self.source_service.fetch_or_fallback(self.settings.world_sources, fallback)
        return AgentResponse(
            agent=self.name,
            summary="World briefing ready.",
            details={
                "coverage": ["Global markets", "US Fed/rates/inflation", "Oil", "Geopolitics", "Regulation", "Technology policy"],
                "relevance": "Signals that can spill into Indian markets, INR, IT exports, and tech valuations.",
                "headlines": headlines,
                "fallback_used": used_mock,
            },
        )


class BriefAgent(BaseAgent):
    name = "brief"
    supported_commands = {"/brief"}

    def __init__(self, market_agent: MarketAgent, news_agent: NewsAgent, world_agent: WorldAgent) -> None:
        self.market_agent = market_agent
        self.news_agent = news_agent
        self.world_agent = world_agent

    async def handle(self, request: AgentRequest) -> AgentResponse:
        market = await self.market_agent.handle(request.model_copy(update={"command": "/market"}))
        news = await self.news_agent.handle(request.model_copy(update={"command": "/news"}))
        world = await self.world_agent.handle(request.model_copy(update={"command": "/world"}))
        watch_points = [
            "Track RBI/FII-DII and INR trend for domestic risk appetite.",
            "Watch AI infra spend and policy changes affecting builders and listed tech.",
            "Monitor Fed + oil shocks for cross-asset volatility impact on India.",
        ]
        telegram_text = "\n".join(
            [
                "*Daily Brief*",
                "",
                "🇮🇳 India Market",
                f"• {market.details['headlines'][0]['title']}",
                "",
                "🤖 AI & Tech",
                f"• {news.details['headlines'][0]['title']}",
                "",
                "🌍 World",
                f"• {world.details['headlines'][0]['title']}",
                "",
                "👀 Watch points",
                "• " + "\n• ".join(watch_points),
            ]
        )
        return AgentResponse(
            agent=self.name,
            summary="Daily combined briefing ready.",
            details={
                "market": market.details,
                "news": news.details,
                "world": world.details,
                "top_watch_points": watch_points,
                "telegram_format": telegram_text,
            },
        )


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
