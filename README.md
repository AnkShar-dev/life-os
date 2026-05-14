# life-os Jarvis (MVP)

A production-minded but simple local-first **personal multi-agent assistant** with Telegram as the main interface, FastAPI webhooks for n8n, and explicit human-approval gates for risky actions.

## 1) Recommended architecture

- **Interface Layer**
  - Telegram bot for day-to-day commands.
  - FastAPI endpoints for n8n/webhook orchestration.
- **Router Layer**
  - `RouterAgent` receives commands and dispatches to specialist agents.
- **Specialist Agents**
  - News (AI/tech), Market (India-focused), World, Brief, Trading, Finance, Resume, Job, Instagram.
- **Approval Layer**
  - Central `ApprovalService` creates/decides approval requests.
  - Mandatory approvals for trading execution, job apply, and Instagram publish.
- **Storage Layer**
  - MVP: SQLite repository.
  - Future: Google Sheets/Postgres adapters behind same interface.
- **Workflow Layer**
  - Scheduler hook module provides daily tasks for cron/n8n.

## 2) Daily briefing milestone (source-driven + fallback)

`/market`, `/news`, `/world`, and `/brief` use a source/adapters layer that fetches configured RSS feeds and gracefully falls back to deterministic mock content when sources are missing or unavailable.

- No secrets are hardcoded.
- No live trading is executed by briefing commands.
- `/webhooks/command` remains n8n-compatible for scheduled calls.

### Brief command coverage
- `/market`: India market brief (`Nifty 50`, `Sensex`, `Bank Nifty`, sector and macro context including RBI/FII-DII/oil/INR).
- `/news`: AI/tech headlines, builder relevance, investor relevance, and why-it-matters.
- `/world`: Global markets, Fed/rates/inflation, oil, geopolitics, regulation, technology policy, and India relevance.
- `/brief`: Combined sectioned brief + top 3 watch points + concise Telegram-friendly output.

## 3) Source configuration (environment variables)

All env vars use the `APP_` prefix.

- `APP_MARKET_SOURCES` (list of RSS URLs)
- `APP_NEWS_SOURCES` (list of RSS URLs)
- `APP_WORLD_SOURCES` (list of RSS URLs)
- `APP_ENABLE_MOCK_DATA` (`true`/`false`; fallback behavior is still retained when sources fail)

Example `.env` values:

```bash
APP_MARKET_SOURCES='["https://example.com/india-markets.rss"]'
APP_NEWS_SOURCES='["https://example.com/ai-tech.rss"]'
APP_WORLD_SOURCES='["https://example.com/world-macro.rss"]'
APP_ENABLE_MOCK_DATA=true
```

## 4) Folder structure

```text
life-os/
├── .env.example
├── pyproject.toml
├── README.md
├── data/
├── src/jarvis/
│   ├── main.py
│   ├── agents/
│   │   ├── base.py
│   │   ├── router.py
│   │   └── specialists.py
│   ├── api/
│   │   └── main.py
│   ├── bot/
│   │   └── telegram_bot.py
│   ├── core/
│   │   ├── config.py
│   │   └── logging.py
│   ├── schemas/
│   │   └── common.py
│   ├── services/
│   │   ├── approval.py
│   │   └── briefing_sources.py
│   ├── storage/
│   │   └── repository.py
│   └── workflows/
│       └── scheduler.py
└── tests/
```

## 5) Setup & run

### Prerequisites
- Python 3.11+

### Install
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

### Configure
```bash
cp .env.example .env
# set APP_TELEGRAM_BOT_TOKEN and optional APP_*_SOURCES vars
```

### Run FastAPI
```bash
uvicorn jarvis.api.main:app --reload
```

### Run Telegram bot
```bash
python -c "from jarvis.main import run_telegram; run_telegram()"
```

## 6) n8n-ready `/brief` schedule example (documentation only)

Call this every morning from an n8n `HTTP Request` node:

```bash
curl -X POST http://127.0.0.1:8000/webhooks/command \
  -H 'content-type: application/json' \
  -d '{"command":"/brief","user_id":"n8n-scheduler","payload":{}}'
```

## 7) Example API calls

### Route a command
```bash
curl -X POST http://127.0.0.1:8000/webhooks/command \
  -H 'content-type: application/json' \
  -d '{"command":"/news","user_id":"me","payload":{}}'
```

### Approve/reject risky action
```bash
curl -X POST http://127.0.0.1:8000/webhooks/approval \
  -H 'content-type: application/json' \
  -d '{"approval_id":"<id>","decision":"approve","decided_by":"me"}'
```

## 8) Tests (no network dependency)

Run full suite:

```bash
pytest
```

Run concise mode:

```bash
pytest -q
```

Briefing tests use fake/mock adapters and do not call external networks.

## 9) Manual test of `/brief`

```bash
curl -X POST http://127.0.0.1:8000/webhooks/command \
  -H 'content-type: application/json' \
  -d '{"command":"/brief"}'
```

## 10) Current mock/fallback scope

- If configured sources are missing, unreachable, or invalid, Jarvis returns structured mock fallback bullets.
- Source labels are included where available.
- This milestone does not add broker execution or any live trading action.
