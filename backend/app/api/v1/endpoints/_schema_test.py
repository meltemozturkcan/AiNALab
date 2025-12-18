from fastapi import APIRouter
from app.schemas.session import CreateSessionRequest
from app.schemas.session_runtime import SessionRuntimeCreateRequest

router = APIRouter(tags=["schema-test"])

@router.post("/_schema-test/session")
async def schema_test_session(payload: CreateSessionRequest):
    # sadece validate edip geri döner
    return {"ok": True}

@router.post("/_schema-test/runtime")
async def schema_test_runtime(payload: SessionRuntimeCreateRequest):
    return {"ok": True}
