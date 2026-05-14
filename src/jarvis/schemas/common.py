"""Shared schemas for agent I/O and approvals."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class AgentRequest(BaseModel):
    command: str
    user_id: str = "local-user"
    payload: dict[str, Any] = Field(default_factory=dict)


class AgentResponse(BaseModel):
    agent: str
    summary: str
    details: dict[str, Any] = Field(default_factory=dict)


class ApprovalRequest(BaseModel):
    approval_id: str
    action_type: str
    payload: dict[str, Any]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = "pending"


class ApprovalDecision(BaseModel):
    approval_id: str
    decision: str
    decided_by: str = "local-user"
