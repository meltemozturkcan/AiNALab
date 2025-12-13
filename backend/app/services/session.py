from datetime import date, datetime, timezone
from uuid import uuid4

from app.db.repositories.session import SessionRepository


def _calculate_age(birth_date: date, today: date) -> tuple[int, int, int]:
    years = today.year - birth_date.year
    months = today.month - birth_date.month

    if today.day < birth_date.day:
        months -= 1

    if months < 0:
        years -= 1
        months += 12

    total_months = years * 12 + months
    return years, months, total_months


class SessionService:
    def __init__(self, repo: SessionRepository):
        self._repo = repo

    async def create_session(self, birth_date: date, gender: str) -> dict:
        today = date.today()
        age_years, age_months, total_months = _calculate_age(birth_date, today)

        doc = {
            "session_id": str(uuid4()),
            "age_years": age_years,
            "age_months": age_months,
            "total_months": total_months,
            "gender": gender,
            "created_at": datetime.now(timezone.utc),
            "status": "active",
        }

        # ⚠️ birth_date burada yok → DB’ye gitmiyor
        return await self._repo.create(doc)
