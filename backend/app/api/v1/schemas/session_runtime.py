"""
Session runtime schemas (temporary, TTL-enabled).
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class SessionRuntimeProgress(BaseModel):
    model_config = ConfigDict(extra="forbid")

    next_letter_index: int = Field(default=0, ge=0)
    next_repeat_index: int = Field(default=0, ge=0)
    completed_recordings: int = Field(default=0, ge=0)
    last_success_at: Optional[datetime] = Field(default=None)


class SessionRuntimeCreateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    session_id: str = Field(..., min_length=8)
    ttl_seconds: Optional[int] = Field(default=None, ge=60, le=60 * 60 * 24)


class SessionRuntimeCreateResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    runtime_token: str
    session_id: str
    created_at: datetime
    expires_at: datetime
    progress: SessionRuntimeProgress
