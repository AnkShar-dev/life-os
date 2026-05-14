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

## 2) Folder structure

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
│   │   └── approval.py
│   ├── storage/
│   │   └── repository.py
│   └── workflows/
│       └── scheduler.py
└── tests/
```

## 3) MVP implementation plan

1. **Bootstrap core app config and logging** (done).
2. **Define agent contracts and router** (done).
3. **Implement specialist agents with mock adapters** (done).
4. **Add approval workflow abstraction** (done).
5. **Add storage abstraction with SQLite implementation** (done).
6. **Expose FastAPI n8n-compatible endpoints** (done).
7. **Wire Telegram command handlers** (done).
8. **Document setup, runbook, safety model, and extension points** (done).

## 4) Starter code notes

- **Router commands**: `/news` (AI/tech), `/market` (India markets), `/world` (global macro), `/brief` (combined daily briefing), `/finance`, `/resume`, `/jobs`, `/reel`, `/trade`.
- **Approval commands** (wire-up ready): `/approve`, `/reject`.
- **FastAPI webhooks**:
  - `POST /webhooks/command`
  - `POST /webhooks/approval`
- **Safety constraint**:
  - Trading/job apply/Instagram posting create approval records and stop at pending state.

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
# set APP_TELEGRAM_BOT_TOKEN
```

### Run FastAPI
```bash
uvicorn jarvis.api.main:app --reload
```

### Run Telegram bot
```bash
python -c "from jarvis.main import run_telegram; run_telegram()"
```

## Example API calls

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

## Telegram commands
- `/news`
- `/market`
- `/world`
- `/brief`
- `/finance`
- `/resume`
- `/jobs`
- `/reel`
- `/approve`
- `/reject`

## Future improvements
- Real API integrations for news/markets/jobs/Instagram.
- OAuth + secure secret management.
- Postgres + migrations.
- Better NLP intent parsing beyond command routing.
- Backtesting and stricter risk policy engine.
- Resume templating + PDF export.


## Manual testing checklist

1. Start API server: `uvicorn jarvis.api.main:app --reload`
2. Verify health: `curl http://127.0.0.1:8000/health`
3. Test briefing commands through webhook:
   - `curl -X POST http://127.0.0.1:8000/webhooks/command -H "content-type: application/json" -d '{"command":"/market"}'`
   - `curl -X POST http://127.0.0.1:8000/webhooks/command -H "content-type: application/json" -d '{"command":"/news"}'`
   - `curl -X POST http://127.0.0.1:8000/webhooks/command -H "content-type: application/json" -d '{"command":"/world"}'`
   - `curl -X POST http://127.0.0.1:8000/webhooks/command -H "content-type: application/json" -d '{"command":"/brief"}'`
4. In Telegram, verify `/market`, `/news`, `/world`, and `/brief` all return message text.

