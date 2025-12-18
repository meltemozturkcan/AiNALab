"""
MongoDB connection management (Motor).

- Runtime imports are kept minimal to avoid type-checker issues.
- Types are expressed using Protocol + Any to keep Pylance happy,
  while runtime behavior remains correct.
"""

import logging
from typing import Any, Optional, Protocol

from motor.motor_asyncio import AsyncIOMotorClient

from app.config import settings

logger = logging.getLogger(__name__)


# --- Minimal "type shape" definitions (Pylance-proof) -------------------------

class _MongoAdmin(Protocol):
    async def command(self, *args: Any, **kwargs: Any) -> Any: ...


class _MongoClient(Protocol):
    admin: _MongoAdmin
    def __getitem__(self, name: str) -> Any: ...
    def close(self) -> None: ...


class _MongoDatabase(Protocol):
    # We keep it intentionally generic; collections will be db["name"] or db.name
    def __getattr__(self, name: str) -> Any: ...
    def __getitem__(self, name: str) -> Any: ...


# --- Database manager ---------------------------------------------------------

class DatabaseManager:
    """MongoDB connection manager (Motor async client)."""

    def __init__(self) -> None:
        self._client: Optional[_MongoClient] = None
        self._db: Optional[_MongoDatabase] = None

    async def connect(self) -> None:
        """Connect to MongoDB and select database."""
        logger.info("🔗 Connecting to MongoDB...")

        # Motor client (real runtime object)
        client = AsyncIOMotorClient(
            settings.mongodb_url,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=5000,
        )

        # Select DB
        db = client[settings.mongodb_db_name]

        # Test connection
        await client.admin.command("ping")

        self._client = client  # type: ignore[assignment]
        self._db = db          # type: ignore[assignment]

        logger.info("✅ Connected to MongoDB successfully")

    async def disconnect(self) -> None:
        """Disconnect MongoDB client."""
        if self._client:
            logger.info("🔌 Disconnecting from MongoDB...")
            self._client.close()
            logger.info("✅ Disconnected from MongoDB")
        self._client = None
        self._db = None

    async def ping(self) -> bool:
        """Return True if MongoDB is reachable."""
        if not self._client:
            return False
        try:
            await self._client.admin.command("ping")
            return True
        except Exception:
            return False

    def get_database(self) -> _MongoDatabase:
        """Get the connected DB handle."""
        if self._db is None:
            raise RuntimeError("Database not connected. Call connect() first.")
        return self._db


# Global instance
db_manager = DatabaseManager()


async def get_database() -> _MongoDatabase:
    """FastAPI dependency to obtain DB handle."""
    return db_manager.get_database()
