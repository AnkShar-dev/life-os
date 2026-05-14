"""Source adapters and fallback service for daily briefings."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET


@dataclass(frozen=True, slots=True)
class SourceItem:
    title: str
    source: str
    link: str = ""


class RssSourceAdapter:
    """Minimal RSS adapter with graceful fallback on failure."""

    def __init__(self, timeout_seconds: float = 5.0) -> None:
        self.timeout_seconds = timeout_seconds

    def fetch(self, url: str, limit: int = 5) -> list[SourceItem]:
        req = Request(url, headers={"User-Agent": "JarvisBriefing/1.0"})
        with urlopen(req, timeout=self.timeout_seconds) as response:  # nosec B310
            payload = response.read()

        root = ET.fromstring(payload)
        channel = root.find("channel")
        if channel is None:
            return []

        entries: list[SourceItem] = []
        for item in channel.findall("item")[:limit]:
            title = (item.findtext("title") or "").strip()
            link = (item.findtext("link") or "").strip()
            source = (item.findtext("source") or "RSS").strip() or "RSS"
            if title:
                entries.append(SourceItem(title=title, source=source, link=link))
        return entries


class BriefingSourceService:
    """Aggregates live-source data with deterministic mock fallback."""

    def __init__(self, adapter: RssSourceAdapter | None = None) -> None:
        self.adapter = adapter or RssSourceAdapter()

    def fetch_or_fallback(self, urls: list[str], fallback: list[dict[str, str]], limit: int = 5) -> tuple[list[dict[str, str]], bool]:
        if not urls:
            return fallback[:limit], True

        items: list[dict[str, str]] = []
        for url in urls:
            try:
                for entry in self.adapter.fetch(url, limit=limit):
                    items.append({"title": entry.title, "source": entry.source, "link": entry.link})
            except Exception:
                continue

        if not items:
            return fallback[:limit], True

        return items[:limit], False

    @staticmethod
    def labels(items: list[dict[str, Any]]) -> list[str]:
        return [str(it.get("source", "Unknown")) for it in items]
