from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.db.indexes import ensure_indexes
from app.db.mongodb import db_manager
from app.api.v1.endpoints import health
from app.api.v1.endpoints import health, sessions


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_manager.connect()
    yield
    await db_manager.disconnect()


app = FastAPI(
    title="Child Voice Recorder API",
    version="0.1.0",
    lifespan=lifespan,
)

# Routers
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(sessions.router, prefix="/api/v1", tags=["sessions"])


@app.get("/")
async def root():
    return {"message": "Child Voice Recorder API is running"}
