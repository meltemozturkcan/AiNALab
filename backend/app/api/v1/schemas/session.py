"""
Session runtime schemas (temporary, TTL-enabled).

- runtime_token is a temporary capability token (UUID).
- progress is NOT research data; it only supports resume UX.
- TTL is enforced at DB level via expires_at index (expireAfterSeconds=0).
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class SessionRuntimeProgress(BaseModel):
    model_config = ConfigDict(extra="forbid")

    next_letter_index: int = Field(default=0, ge=0, description="Next letter index to record.")
    next_repeat_index: int = Field(default=0, ge=0, description="Next repeat index for the current letter.")
    completed_recordings: int = Field(default=0, ge=0, description="How many recordings completed in this runtime.")
    last_success_at: Optional[datetime] = Field(default=None, description="Last successful operation timestamp (UTC).")


class SessionRuntimeCreateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    session_id: str = Field(..., min_length=8, description="Persistent research session_id reference (UUID).")
    ttl_seconds: Optional[int] = Field(
        default=None,
        ge=60,
        le=60 * 60 * 24,
        description="Optional TTL override (60s..86400s). If omitted, server default is used.",
    )


class SessionRuntimeCreateResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    runtime_token: str = Field(..., description="Temporary runtime token (UUID).")
    session_id: str = Field(..., description="Persistent research session_id reference (UUID).")
    created_at: datetime = Field(..., description="UTC timestamp when runtime token created.")
    expires_at: datetime = Field(..., description="UTC timestamp when runtime token expires (TTL).")
    progress: SessionRuntimeProgress
