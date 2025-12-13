from pymongo import ASCENDING

TTL_SECONDS = 60 * 60 * 24  # 86400

def ensure_indexes(db):
    db.sessions.create_index(
        [("created_at", ASCENDING)],
        expireAfterSeconds=TTL_SECONDS,
        name="ttl_sessions_created_at_24h"
    )