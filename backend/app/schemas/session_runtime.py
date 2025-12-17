"""
Session runtime schemas (temporary, TTL-enabled).

Runtime = geçici oturum (TTL ile silinir).
Kalıcı demografi (birth_month/year) runtime'da taşınmaz.
Progress backend otoritesidir; UI yalnızca "niyet" bildirir.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class SessionRuntimeProgress(BaseModel):
    model_config = ConfigDict(extra="forbid")

    # Backend truth:
    # ok_count == completed_recordings (0..58)
    completed_recordings: int = Field(default=0, ge=0, le=58)

    # "completed" backend tarafından ok_count üzerinden belirlenir
    completed: bool = Field(default=False)

    # Next-step (completed değilse dolu olmalı)
    next_letter_index: int = Field(default=0, ge=0, le=28)
    next_repeat_index: int = Field(default=1, ge=1, le=2)

    last_success_at: Optional[datetime] = Field(default=None)


class SessionRuntimeCreateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    session_id: str = Field(..., min_length=8)

    # TTL için opsiyon (örn. 1 saat = 3600)
    ttl_seconds: Optional[int] = Field(default=None, ge=60, le=60 * 60 * 24)


class SessionRuntimeCreateResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    runtime_token: str
    session_id: str
    created_at: datetime
    expires_at: datetime
    progress: SessionRuntimeProgress
