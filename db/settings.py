import aiosqlite

DB_PATH = "bot.db"

async def set_chat_setting(chat_id: int, key: str, value: str | None) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        if value is None:
            await db.execute(
                "DELETE FROM settings WHERE chat_id=? AND key=?",
                (chat_id, key),
            )
        else:
            await db.execute(
                "REPLACE INTO settings (chat_id, key, value) VALUES (?, ?, ?)",
                (chat_id, key, value),
            )
        await db.commit()

async def get_chat_setting(chat_id: int, key: str, default=None):
    async with aiosqlite.connect(DB_PATH) as db:
        row = await db.execute_fetchone(
            "SELECT value FROM settings WHERE chat_id=? AND key=?",
            (chat_id, key),
        )
        return row[0] if row else default
