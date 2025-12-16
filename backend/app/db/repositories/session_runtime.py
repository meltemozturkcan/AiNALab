from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional
from uuid import uuid4


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class SessionRuntimeRepository:
    def __init__(self, db: Any):
        self._runtime = db["session_runtime"]
        self._sessions = db["sessions"]
        self._default_ttl_seconds = int(os.getenv("SESSION_RUNTIME_TTL_SECONDS", "3600"))

    async def session_exists(self, session_id: str) -> bool:
        doc = await self._sessions.find_one({"session_id": session_id}, {"_id": 1})
        return doc is not None

    async def create_runtime(self, session_id: str, ttl_seconds: Optional[int] = None) -> Dict[str, Any]:
        if not await self.session_exists(session_id):
            raise ValueError("SESSION_NOT_FOUND")

        now = _utcnow()
        ttl = ttl_seconds if ttl_seconds is not None else self._default_ttl_seconds
        expires_at = now + timedelta(seconds=ttl)

        doc: Dict[str, Any] = {
            "runtime_token": str(uuid4()),
            "session_id": session_id,
            "progress": {
                "next_letter_index": 0,
                "next_repeat_index": 0,
                "completed_recordings": 0,
                "last_success_at": None,
            },
            "created_at": now,
            "expires_at": expires_at,
        }

        await self._runtime.insert_one(doc)
        doc.pop("_id", None)
        return doc
