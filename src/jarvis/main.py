"""CLI helpers to run local Jarvis components."""

import asyncio

from jarvis.bot.telegram_bot import run_bot


def run_telegram() -> None:
    asyncio.run(run_bot())
