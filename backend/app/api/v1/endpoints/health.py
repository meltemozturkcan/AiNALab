from fastapi import APIRouter
from app.db.mongodb import db_manager

router = APIRouter()

@router.get("/health")
async def health_check():
    db_ok = await db_manager.ping()
    return {"status": "ok" if db_ok else "degraded", "mongodb": db_ok}
