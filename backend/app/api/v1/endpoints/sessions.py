from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.session import (
    CreateSessionRequest,
    CreateSessionResponse,
)
from app.db.mongodb import get_database


router = APIRouter(tags=["sessions"])

