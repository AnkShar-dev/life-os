"""Storage abstraction with SQLite implementation for MVP."""

from __future__ import annotations

import json
import sqlite3
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
