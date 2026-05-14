"""Storage abstraction with SQLite implementation for MVP."""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


class SQLiteRepository:
    """Simple SQLite-backed repository for logs and approvals."""

    def __init__(self, db_path: str) -> None:
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self._db_path = db_path
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self._db_path)

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(
                "CREATE TABLE IF NOT EXISTS approvals (id TEXT PRIMARY KEY, action_type TEXT, payload TEXT, status TEXT)"
            )
            conn.execute(
                "CREATE TABLE IF NOT EXISTS trade_logs (id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT)"
            )
            conn.execute(
                "CREATE TABLE IF NOT EXISTS resume_versions (id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT)"
            )

    def save_approval(self, approval_id: str, action_type: str, payload: dict[str, Any]) -> None:
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO approvals (id, action_type, payload, status) VALUES (?, ?, ?, ?)",
                (approval_id, action_type, json.dumps(payload), "pending"),
            )

    def set_approval_status(self, approval_id: str, status: str) -> None:
        with self._connect() as conn:
            conn.execute("UPDATE approvals SET status = ? WHERE id = ?", (status, approval_id))

    def log_trade(self, payload: dict[str, Any]) -> None:
        with self._connect() as conn:
            conn.execute("INSERT INTO trade_logs (content) VALUES (?)", (json.dumps(payload),))

    def save_resume_version(self, payload: dict[str, Any]) -> None:
        with self._connect() as conn:
            conn.execute("INSERT INTO resume_versions (content) VALUES (?)", (json.dumps(payload),))


@dataclass(order=True)
class ApprovalItem:
    request_id: str
    approved_by: list[str] = field(default_factory=list)


class ApprovalRepository:
    def __init__(self) -> None:
        self._items: dict[str, ApprovalItem] = {}

    def request(self, request_id: str) -> None:
        self._items.setdefault(request_id, ApprovalItem(request_id=request_id))

    def approve(self, request_id: str, approver: str) -> None:
        item = self._items.setdefault(request_id, ApprovalItem(request_id=request_id))
        if approver not in item.approved_by:
            item.approved_by.append(approver)

    def status(self, request_id: str, required_approvers: set[str]) -> dict[str, object]:
        item = self._items.setdefault(request_id, ApprovalItem(request_id=request_id))
        approved = required_approvers.issubset(set(item.approved_by))
        return {"approved": approved, "approved_by": item.approved_by}

    def list_pending(self) -> list[ApprovalItem]:
        return [self._items[k] for k in sorted(self._items)]
