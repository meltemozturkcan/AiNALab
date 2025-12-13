"""
Session request/response schemas (privacy-first).

- birth_date is accepted ONLY to compute age metrics.
- birth_date is NEVER stored in DB.
"""

from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, Field, ConfigDict


Gender = Literal["male", "female", "unspecified"]


class SessionCreateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    birth_date: date = Field(
        ...,
        description="Used only for age calculation. Never stored.",
        examples=["2021-08-15"],
    )

    gender: Gender = Field(
        default="unspecified",
        description="Optional gender field (limited values).",
        examples=["female"],
    )


class SessionCreateResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    session_id: str = Field(..., description="Anonymous session identifier (UUID).")
    age_years: int = Field(..., ge=0, le=10, description="Completed years.")
    age_months: int = Field(..., ge=0, le=11, description="Remaining months (0-11).")
    total_months: int = Field(..., ge=0, le=120, description="Total age in months.")
    gender: Gender
    created_at: datetime
    status: Literal["active"] = "active"
