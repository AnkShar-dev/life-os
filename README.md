# life-os

Personal multi-agent AI assistant for productivity, finance, jobs, and content automation.

## Architecture

Primary implementation lives under `src/jarvis`.

This branch currently focuses on:
- Telegram hardening in `src/jarvis/bot/telegram_bot.py`
- End-to-end approval flow in `src/jarvis/services/approval.py`
- Pending approval storage/listing in `src/jarvis/storage/repository.py`
- Daily briefing formatting in `src/jarvis/workflows/daily_briefing_formatter.py`
- Tests in `tests/` importing only `jarvis` modules
