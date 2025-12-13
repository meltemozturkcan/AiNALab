from app.db.mongodb import _MongoDatabase


class SessionRepository:
    def __init__(self, db: _MongoDatabase):
        self._col = db["sessions"]

    async def create(self, doc: dict) -> dict:
        result = await self._col.insert_one(doc)

        # Mongo _id'yi DB tarafında tut, API response'a sokma
        # (istersen internal log için kullanabilirsin)
        doc.pop("_id", None)

        return doc

