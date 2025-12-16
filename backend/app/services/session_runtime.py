from __future__ import annotations

from typing import Any, Dict, Optional

from app.db.repositories.session_runtime import SessionRuntimeRepository


class SessionRuntimeService:
    def __init__(self, repo: SessionRuntimeRepository):
        self._repo = repo

    async def create_runtime(self, session_id: str, ttl_seconds: Optional[int] = None) -> Dict[str, Any]:
        return await self._repo.create_runtime(session_id=session_id, ttl_seconds=ttl_seconds)
