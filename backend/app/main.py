from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.db.indexes import ensure_indexes
from app.db.mongodb import db_manager
from app.api.v1.endpoints import health, sessions, session_runtime


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1) DB bağlan
    await db_manager.connect()

    # 2) Indexleri kur (idempotent)
    db = db_manager.get_database()
    await ensure_indexes(db)

    # 3) App çalışsın
    yield

    # 4) Kapatırken DB bağlantısını kapat
    await db_manager.disconnect()


app = FastAPI(
    title="Child Voice Recorder API",
    version="0.1.0",
    lifespan=lifespan,
)

# Routers
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(sessions.router, prefix="/api/v1", tags=["sessions"])
app.include_router(session_runtime.router, prefix="/api/v1", tags=["session-runtime"])


@app.get("/")
async def root():
    return {"message": "Child Voice Recorder API is running"}
