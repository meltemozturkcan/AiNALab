from __future__ import annotations

from pymongo import ASCENDING, DESCENDING


async def ensure_indexes(db) -> None:
    """
    Phase-1 index bootstrap (idempotent).

    Rules:
    - sessions: NO TTL
    - session_runtime: TTL ONLY here
    - recordings: idempotency guaranteed by unique compound index
    """

    # ---------------------------------------------------------------------
    # SESSIONS (persistent research sessions)
    # ---------------------------------------------------------------------

    await db.sessions.create_index(
        [("created_at", DESCENDING)],
        name="idx_sessions_created_at_desc",
    )

    # ---------------------------------------------------------------------
    # SESSION_RUNTIME (temporary, TTL-enabled)
    # ---------------------------------------------------------------------

    runtime = db.session_runtime

    # TTL: runtime expires automatically
    await runtime.create_index(
        [("expires_at", ASCENDING)],
        expireAfterSeconds=0,
        name="ttl_session_runtime_expires_at",
    )

    # runtime_token capability (keep for now)
    await runtime.create_index(
        [("runtime_token", ASCENDING)],
        unique=True,
        name="uq_session_runtime_runtime_token",
    )

    # resume / lookup by session_id
    await runtime.create_index(
        [("session_id", ASCENDING)],
        name="idx_session_runtime_session_id",
    )

    # ---------------------------------------------------------------------
    # RECORDINGS (research data)
    # ---------------------------------------------------------------------

    # Idempotency invariant (I1):
    # One recording per (session_id, letter_index, repeat_index)
    await db.recordings.create_index(
        [("session_id", ASCENDING), ("letter_index", ASCENDING), ("repeat_index", ASCENDING)],
        unique=True,
        name="uq_recordings_session_letter_repeat",
    )

    # Admin / debug / pagination
    await db.recordings.create_index(
        [("session_id", ASCENDING), ("created_at", DESCENDING)],
        name="idx_recordings_session_created_desc",
    )

    await db.recordings.create_index(
        [("created_at", DESCENDING)],
        name="idx_recordings_created_desc",
    )

    await db.recordings.create_index(
        [("transcription_status", ASCENDING), ("created_at", DESCENDING)],
        name="idx_recordings_transcription_created_desc",
    )

    await db.recordings.create_index(
        [("labels_status", ASCENDING), ("created_at", DESCENDING)],
        name="idx_recordings_labels_created_desc",
    )
