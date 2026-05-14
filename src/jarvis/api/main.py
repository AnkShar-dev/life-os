"""FastAPI app exposing n8n-compatible webhooks."""

from fastapi import FastAPI

from jarvis.agents.router import RouterAgent
from jarvis.agents.specialists import (
    FinanceAgent,
    InstagramAgent,
    JobAgent,
    MarketAgent,
    NewsAgent,
    ResumeAgent,
    TradingAgent,
    WorldAgent,
    BriefAgent,
)
from jarvis.core.config import get_settings
from jarvis.core.logging import setup_logging
from jarvis.schemas.common import AgentRequest, ApprovalDecision
from jarvis.services.approval import ApprovalService
from jarvis.storage.repository import SQLiteRepository

settings = get_settings()
setup_logging(settings.log_level)
repo = SQLiteRepository(settings.sqlite_path)
approvals = ApprovalService(repo)
news_agent = NewsAgent()
market_agent = MarketAgent()
world_agent = WorldAgent()

router = RouterAgent(
    [
        news_agent,
        market_agent,
        world_agent,
        BriefAgent(market_agent, news_agent, world_agent),
        TradingAgent(approvals, repo),
        FinanceAgent(),
        ResumeAgent(repo),
        JobAgent(approvals),
        InstagramAgent(approvals),
    ]
)

app = FastAPI(title="Jarvis API")


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/webhooks/command")
async def command(request: AgentRequest) -> dict:
    response = await router.route(request)
    return response.model_dump()


@app.post("/webhooks/approval")
async def approval(decision: ApprovalDecision) -> dict[str, str]:
    status = approvals.decide(decision)
    return {"approval_id": decision.approval_id, "status": status}
