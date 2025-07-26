import aiosqlite
import asyncio
import logging

DB_PATH = "bot.db"

CREATE_TABLES = [
    """
    CREATE TABLE IF NOT EXISTS warns (
        chat_id INTEGER,
        user_id INTEGER,
        count INTEGER DEFAULT 0,
        PRIMARY KEY (chat_id, user_id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS settings (
        chat_id INTEGER,
        key TEXT,
        value TEXT,
        PRIMARY KEY (chat_id, key)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS notes (
        chat_id INTEGER,
        name TEXT,
        content TEXT,
        PRIMARY KEY (chat_id, name)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS approvals (
        chat_id INTEGER,
        user_id INTEGER,
        PRIMARY KEY (chat_id, user_id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS broadcast_users (
        user_id INTEGER PRIMARY KEY
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS broadcast_groups (
        group_id INTEGER PRIMARY KEY
    )
    """
]


logger = logging.getLogger(__name__)
_db_lock = asyncio.Lock()
_initialized = False


async def init_db() -> None:
    """Initialize the SQLite database once."""
    global _initialized
    async with _db_lock:
        if _initialized:
            return
        try:
            async with aiosqlite.connect(DB_PATH) as db:
                for query in CREATE_TABLES:
                    await db.execute(query)
                await db.commit()
            _initialized = True
            logger.info("Database initialized")
        except Exception as e:
            logger.exception("Failed to initialize database: %s", e)
            raise
