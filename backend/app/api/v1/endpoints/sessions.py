from fastapi import APIRouter, Depends, status

from app.api.v1.schemas.session import SessionCreateRequest, SessionCreateResponse
from app.db.mongodb import get_database
from app.db.repositories.session import SessionRepository
from app.services.session import SessionService

router = APIRouter()


@router.post("/sessions", response_model=SessionCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_session(payload: SessionCreateRequest, db=Depends(get_database)):
    repo = SessionRepository(db)
    service = SessionService(repo)
    return await service.create_session(payload.birth_date, payload.gender)
