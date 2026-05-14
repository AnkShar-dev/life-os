import asyncio

from jarvis.api.main import router
from jarvis.schemas.common import AgentRequest


def test_briefing_routes():
    for command, expected_agent in [("/market", "market"), ("/news", "news"), ("/world", "world"), ("/brief", "brief")]:
        response = asyncio.run(router.route(AgentRequest(command=command)))
        assert response.agent == expected_agent


def test_market_output_is_india_focused():
    response = asyncio.run(router.route(AgentRequest(command="/market")))
    assert "Nifty 50" in response.details["indices"]
    assert "Sensex" in response.details["indices"]
    assert "Bank Nifty" in response.details["indices"]
    assert "RBI" in response.details["macro"]


def test_news_output_is_ai_tech_focused():
    response = asyncio.run(router.route(AgentRequest(command="/news")))
    assert "AI & tech" in response.summary
    assert "Technology and AI" in response.details["focus"]


def test_world_output_covers_global_market_tech_geopolitics_and_regulation():
    response = asyncio.run(router.route(AgentRequest(command="/world")))
    coverage = response.details["coverage"]
    assert "Global markets" in coverage
    assert "Technology policy" in coverage
    assert "Oil" in coverage
    assert "Geopolitics" in coverage
    assert "Regulation" in coverage


def test_brief_combines_market_news_and_world_for_telegram():
    response = asyncio.run(router.route(AgentRequest(command="/brief")))
    assert "market" in response.details
    assert "news" in response.details
    assert "world" in response.details
    assert "n8n" in response.details["telegram_format"]
