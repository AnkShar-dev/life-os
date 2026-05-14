# life-os

Personal multi-agent AI assistant for productivity, finance, jobs, and content automation.

## Primary Architecture

The only primary implementation architecture is under `src/jarvis`.

## PR #2 Conflict Resolution Notes

This PR keeps the `src/jarvis` architecture and preserves the PR #2 functionality:

- **Telegram hardening** in `src/jarvis/bot/telegram_bot.py` with token checks and destination allowlisting.
- **Approval flow** in `src/jarvis/services/approval.py` with request/approve/status behavior.
- **Pending approval storage/listing** in `src/jarvis/storage/repository.py` through `ApprovalRepository` and `list_pending()`.
- **Daily briefing formatter** in `src/jarvis/workflows/daily_briefing_formatter.py`.
- **Tests** in `tests/` importing only `jarvis` modules.

## Repository Layout

- `src/jarvis/bot/` — bot-facing integrations and security checks
- `src/jarvis/services/` — domain services and workflow orchestration
- `src/jarvis/storage/` — repository/storage abstractions
- `src/jarvis/workflows/` — workflow formatting and presentation logic
- `tests/` — automated tests for `jarvis` modules
