import time
import aiosqlite

DB_PATH = "bot.db"

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS warns (
    user_id INTEGER,
    chat_id INTEGER,
    warn_count INTEGER DEFAULT 0,
    last_warn_time INTEGER,
    PRIMARY KEY(user_id, chat_id)
)
"""

async def ensure_table(db):
    await db.execute(CREATE_TABLE_SQL)

async def add_warn(user_id: int, chat_id: int) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        await ensure_table(db)
        cur = await db.execute(
            "SELECT warn_count FROM warns WHERE user_id=? AND chat_id=?",
            (user_id, chat_id)
        )
        row = await cur.fetchone()
        count = (row[0] + 1) if row else 1
        if row:
            await db.execute(
                "UPDATE warns SET warn_count=?, last_warn_time=? WHERE user_id=? AND chat_id=?",
                (count, int(time.time()), user_id, chat_id)
            )
        else:
            await db.execute(
                "INSERT INTO warns(user_id, chat_id, warn_count, last_warn_time) VALUES (?, ?, ?, ?)",
                (user_id, chat_id, count, int(time.time()))
            )
        await db.commit()
        return count

async def get_warns(user_id: int, chat_id: int) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        await ensure_table(db)
        cur = await db.execute(
            "SELECT warn_count FROM warns WHERE user_id=? AND chat_id=?",
            (user_id, chat_id)
        )
        row = await cur.fetchone()
        return row[0] if row else 0

async def reset_warns(user_id: int, chat_id: int) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await ensure_table(db)
        await db.execute(
            "DELETE FROM warns WHERE user_id=? AND chat_id=?",
            (user_id, chat_id)
        )
        await db.commit()

async def remove_warn(user_id: int, chat_id: int) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        await ensure_table(db)
        cur = await db.execute(
            "SELECT warn_count FROM warns WHERE user_id=? AND chat_id=?",
            (user_id, chat_id)
        )
        row = await cur.fetchone()
        if not row:
            return 0
        count = max(row[0] - 1, 0)
        if count == 0:
            await db.execute(
                "DELETE FROM warns WHERE user_id=? AND chat_id=?",
                (user_id, chat_id)
            )
        else:
            await db.execute(
                "UPDATE warns SET warn_count=? WHERE user_id=? AND chat_id=?",
                (count, user_id, chat_id)
            )
        await db.commit()
        return count
