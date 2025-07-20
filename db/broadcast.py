import aiosqlite

DB_PATH = "bot.db"

async def add_user(user_id: int) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR IGNORE INTO broadcast_users(user_id) VALUES(?)",
            (user_id,),
        )
        await db.commit()

async def add_group(group_id: int) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR IGNORE INTO broadcast_groups(group_id) VALUES(?)",
            (group_id,),
        )
        await db.commit()

async def remove_group(group_id: int) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "DELETE FROM broadcast_groups WHERE group_id=?",
            (group_id,),
        )
        await db.commit()

async def get_broadcast_users() -> list[int]:
    async with aiosqlite.connect(DB_PATH) as db:
        rows = await db.execute_fetchall("SELECT user_id FROM broadcast_users")
        return [r[0] for r in rows]

async def get_broadcast_groups() -> list[int]:
    async with aiosqlite.connect(DB_PATH) as db:
        rows = await db.execute_fetchall("SELECT group_id FROM broadcast_groups")
        return [r[0] for r in rows]
