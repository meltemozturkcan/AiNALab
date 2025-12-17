from __future__ import annotations

from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


Gender = Literal["female", "male", "other", "unknown"]
Jurisdiction = Literal["TR", "EU", "OTHER"]
SessionStatus = Literal["ACTIVE", "COMPLETED"]


class ConsentArtifact(BaseModel):
    """
    PII içermez.
    Consent'in kanıtlanabilir bir artifact olarak saklanması hedeflenir.
    """
    model_config = ConfigDict(extra="forbid")

    consent_version: str = Field(..., min_length=1, max_length=64)
    consent_text_hash: str = Field(..., min_length=16, max_length=128)
    consent_accepted_at: datetime = Field(..., description="UTC timestamp when consent accepted.")
    jurisdiction: Jurisdiction = Field(default="TR")


class Demography(BaseModel):
    """
    birth_month/year kalıcıdır: sessions içinde saklanır, session_runtime’da taşınmaz.
    """
    model_config = ConfigDict(extra="forbid")

    birth_year: int = Field(..., ge=1900, le=2100)
    birth_month: int = Field(..., ge=1, le=12)
    gender: Gender = Field(default="unknown")


class Progress(BaseModel):
    """
    Backend otoritesidir. UI sadece “niyet” bildirir.
    """
    model_config = ConfigDict(extra="forbid")

    ok_count: int = Field(..., ge=0, le=58, description="Count(recordings.OK) for this session.")
    is_completed: bool = Field(..., description="Derived from ok_count == 58.")

    next_letter_index: Optional[int] = Field(default=None, ge=0, le=28)
    next_repeat_index: Optional[int] = Field(default=None, ge=1, le=2)


class CreateSessionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    consent: ConsentArtifact
    demography: Demography


class CreateSessionResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    session_id: str
    session_status: SessionStatus

    runtime_token: str
    runtime_expires_at: datetime

    progress: Progress
