import asyncio

from jarvis.agents.specialists import BriefAgent, MarketAgent, NewsAgent, WorldAgent
from jarvis.core.config import Settings
from jarvis.schemas.common import AgentRequest
from jarvis.services.briefing_sources import BriefingSourceService, SourceItem


class FakeRssAdapter:
    def __init__(self, fail: bool = False):
        self.fail = fail

    def fetch(self, url: str, limit: int = 5):
        if self.fail:
            raise RuntimeError("source down")
        return [SourceItem(title=f"headline from {url}", source="fake-rss", link=url)]


def _agents(adapter: FakeRssAdapter, with_sources: bool = True):
    settings = Settings(
        market_sources=["https://example.com/market.xml"] if with_sources else [],
        news_sources=["https://example.com/news.xml"] if with_sources else [],
        world_sources=["https://example.com/world.xml"] if with_sources else [],
    )
    service = BriefingSourceService(adapter=adapter)
    return (
        MarketAgent(source_service=service, settings=settings),
        NewsAgent(source_service=service, settings=settings),
        WorldAgent(source_service=service, settings=settings),
    )


def test_briefing_routes():
    market, news, world = _agents(FakeRssAdapter())
    brief = BriefAgent(market, news, world)
    for agent, command, expected_agent in [
        (market, "/market", "market"),
        (news, "/news", "news"),
        (world, "/world", "world"),
        (brief, "/brief", "brief"),
    ]:
        response = asyncio.run(agent.handle(AgentRequest(command=command)))
        assert response.agent == expected_agent


def test_market_output_is_india_focused():
    market, _, _ = _agents(FakeRssAdapter())
    response = asyncio.run(market.handle(AgentRequest(command="/market")))
    assert "Nifty 50" in response.details["indices"]
    assert "Sensex" in response.details["indices"]
    assert "Bank Nifty" in response.details["indices"]
    assert "RBI" in response.details["macro_context"]
    assert response.details["fallback_used"] is False


def test_news_output_is_ai_tech_focused():
    _, news, _ = _agents(FakeRssAdapter())
    response = asyncio.run(news.handle(AgentRequest(command="/news")))
    assert "AI & tech" in response.summary
    assert "builder" in response.details["builder_relevance"].lower()
    assert response.details["source_labels"] == ["fake-rss"]


def test_world_output_covers_global_market_tech_geopolitics_and_regulation():
    _, _, world = _agents(FakeRssAdapter())
    response = asyncio.run(world.handle(AgentRequest(command="/world")))
    coverage = response.details["coverage"]
    assert "Global markets" in coverage
    assert "Technology policy" in coverage
    assert "Oil" in coverage
    assert "Geopolitics" in coverage
    assert "Regulation" in coverage


def test_brief_combines_market_news_world_and_watch_points_for_telegram():
    market, news, world = _agents(FakeRssAdapter())
    brief = BriefAgent(market, news, world)
    response = asyncio.run(brief.handle(AgentRequest(command="/brief")))
    assert "market" in response.details
    assert "news" in response.details
    assert "world" in response.details
    assert len(response.details["top_watch_points"]) == 3
    assert "🇮🇳 India Market" in response.details["telegram_format"]
    assert "🤖 AI & Tech" in response.details["telegram_format"]
    assert "🌍 World" in response.details["telegram_format"]
    assert "👀 Watch points" in response.details["telegram_format"]


def test_source_fallback_when_unreachable_or_missing():
    market, news, world = _agents(FakeRssAdapter(fail=True), with_sources=True)
    m = asyncio.run(market.handle(AgentRequest(command="/market")))
    n = asyncio.run(news.handle(AgentRequest(command="/news")))
    w = asyncio.run(world.handle(AgentRequest(command="/world")))
    assert m.details["fallback_used"] is True
    assert n.details["fallback_used"] is True
    assert w.details["fallback_used"] is True

    market2, _, _ = _agents(FakeRssAdapter(), with_sources=False)
    m2 = asyncio.run(market2.handle(AgentRequest(command="/market")))
    assert m2.details["fallback_used"] is True
