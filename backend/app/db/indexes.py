from __future__ import annotations
from pymongo import ASCENDING, DESCENDING




async def ensure_indexes(db) -> None:
    """
    Motor (async) ile indexleri idempotent şekilde kurar.

    PHASE-1 STRATEJİSİ:
    - Mevcut sessions TTL davranışı BOZULMAZ
    - Yeni session_runtime koleksiyonu eklenir
    - TTL yalnızca session_runtime.expires_at üzerinde uygulanır
    """

    # -------------------------------------------------------------------------
    # SESSIONS  (LEGACY – ŞİMDİLİK DOKUNULMAZ)
    # -------------------------------------------------------------------------

   
    

    # created_at sort / admin
    await db.sessions.create_index(
        [("created_at", DESCENDING)],
        name="idx_sessions_created_at_desc",
    )

    # -------------------------------------------------------------------------
    # SESSION_RUNTIME  (YENİ – TTL BURADA)
    # -------------------------------------------------------------------------

    # Runtime oturumları:
    # - Araştırma verisi DEĞİL
    # - Sadece frontend-backend akışı için
    # - TTL ile otomatik silinir
    runtime = db.session_runtime

    # 1) TTL: expires_at geldiğinde runtime otomatik silinir
    await runtime.create_index(
        [("expires_at", ASCENDING)],
        expireAfterSeconds=0,
        name="ttl_session_runtime_expires_at",
    )

    # 2) runtime_token capability olduğu için UNIQUE
    await runtime.create_index(
        [("runtime_token", ASCENDING)],
        unique=True,
        name="uq_session_runtime_runtime_token",
    )

    # 3) session_id lookup (resume / kontrol)
    await runtime.create_index(
        [("session_id", ASCENDING)],
        name="idx_session_runtime_session_id",
    )

    # -------------------------------------------------------------------------
    # RECORDINGS  (MEVCUT)
    # -------------------------------------------------------------------------

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

    # -------------------------------------------------------------------------
    # STATS
    # -------------------------------------------------------------------------

    await db.session_stats_daily.create_index(
        [("day", ASCENDING)],
        name="idx_session_stats_day",
    )
    await db.recording_stats_daily.create_index(
        [("day", ASCENDING)],
        name="idx_recording_stats_day",
    )
