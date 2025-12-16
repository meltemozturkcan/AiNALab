from fastapi import APIRouter, Depends, HTTPException, status

from app.api.v1.schemas.session_runtime import (
    SessionRuntimeCreateRequest,
    SessionRuntimeCreateResponse,
    SessionRuntimeProgress,
)
from app.db.mongodb import get_database
from app.db.repositories.session_runtime import SessionRuntimeRepository
from app.services.session_runtime import SessionRuntimeService

router = APIRouter()


@router.post("/session-runtime", response_model=SessionRuntimeCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_session_runtime(payload: SessionRuntimeCreateRequest, db=Depends(get_database)):
    repo = SessionRuntimeRepository(db)
    service = SessionRuntimeService(repo)

    try:
        doc = await service.create_runtime(payload.session_id, payload.ttl_seconds)
    except ValueError as e:
        if str(e) == "SESSION_NOT_FOUND":
            raise HTTPException(status_code=404, detail="session_id not found")
        raise

    return SessionRuntimeCreateResponse(
        runtime_token=doc["runtime_token"],
        session_id=doc["session_id"],
        created_at=doc["created_at"],
        expires_at=doc["expires_at"],
        progress=SessionRuntimeProgress(**doc["progress"]),
    )
