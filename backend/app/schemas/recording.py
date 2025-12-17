from __future__ import annotations

from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

RecordingStatus = Literal["PENDING", "OK", "FAILED"]


class UploadIntentRequest(BaseModel):
    """
    UI step gönderse bile backend doğrular.
    """
    model_config = ConfigDict(extra="forbid")

    runtime_token: str = Field(..., min_length=10, max_length=256)
    letter_index: int = Field(..., ge=0, le=28)
    repeat_index: int = Field(..., ge=1, le=2)


class UploadIntentResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    recording_id: str
    upload_url: Optional[str] = None  # already OK ise None olabilir
    upload_url_expires_at: Optional[datetime] = None
    blob_path: str
    recording_status: RecordingStatus  # PENDING/FAILED/OK
    # Backend truth (progress)
    ok_count: int = Field(..., ge=0, le=58)
    is_completed: bool
    next_letter_index: Optional[int] = Field(default=None, ge=0, le=28)
    next_repeat_index: Optional[int] = Field(default=None, ge=1, le=2)


class UploadCompletedRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    runtime_token: str = Field(..., min_length=10, max_length=256)
    recording_id: str

    # opsiyonel teknik metrikler (PII değil)
    duration_ms: Optional[int] = Field(default=None, ge=0, le=600_000)
    sample_rate_hz: Optional[int] = Field(default=None, ge=8000, le=96_000)
    bytes_size: Optional[int] = Field(default=None, ge=0, le=200_000_000)


class UploadCompletedResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    recording_id: str
    recording_status: RecordingStatus  # OK (idempotent ise yine OK)
    ok_count: int = Field(..., ge=0, le=58)
    is_completed: bool
    next_letter_index: Optional[int] = Field(default=None, ge=0, le=28)
    next_repeat_index: Optional[int] = Field(default=None, ge=1, le=2)
