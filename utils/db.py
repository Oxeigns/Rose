import sqlite3
from contextlib import closing
import aiosqlite
import asyncio

DB_PATH = 'bot.db'

def init_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    with closing(conn.cursor()) as cur:
        cur.execute('''CREATE TABLE IF NOT EXISTS warnings (
            user_id INTEGER,
            chat_id INTEGER,
            warn_count INTEGER DEFAULT 0,
            timestamp INTEGER
        )''')
        cur.execute('''CREATE TABLE IF NOT EXISTS notes (
            chat_id INTEGER,
            name TEXT,
            content TEXT
        )''')
        cur.execute('''CREATE TABLE IF NOT EXISTS settings (
            chat_id INTEGER,
            key TEXT,
            value TEXT,
            PRIMARY KEY(chat_id, key)
        )''')
        cur.execute('''CREATE TABLE IF NOT EXISTS filters (
            chat_id INTEGER,
            keyword TEXT,
            response TEXT,
            PRIMARY KEY(chat_id, keyword)
        )''')
        conn.commit()
    return conn

conn = init_db()

# -- SETTINGS --

def set_chat_setting(chat_id: int, key: str, value: str) -> None:
    with closing(conn.cursor()) as cur:
        cur.execute(
            'REPLACE INTO settings (chat_id, key, value) VALUES (?, ?, ?)',
            (chat_id, key, value)
        )
        conn.commit()

def get_chat_setting(chat_id: int, key: str, default=None):
    with closing(conn.cursor()) as cur:
        cur.execute(
            'SELECT value FROM settings WHERE chat_id=? AND key=?',
            (chat_id, key)
        )
        row = cur.fetchone()
    return row[0] if row else default

# -- FILTERS --

def add_filter(chat_id: int, keyword: str, response: str) -> None:
    with closing(conn.cursor()) as cur:
        cur.execute(
            'REPLACE INTO filters (chat_id, keyword, response) VALUES (?, ?, ?)',
            (chat_id, keyword.lower(), response)
        )
        conn.commit()

def remove_filter(chat_id: int, keyword: str) -> None:
    with closing(conn.cursor()) as cur:
        cur.execute(
            'DELETE FROM filters WHERE chat_id=? AND keyword=?',
            (chat_id, keyword.lower())
        )
        conn.commit()

def get_filter(chat_id: int, keyword: str):
    with closing(conn.cursor()) as cur:
        cur.execute(
            'SELECT response FROM filters WHERE chat_id=? AND keyword=?',
            (chat_id, keyword.lower())
        )
        row = cur.fetchone()
    return row[0] if row else None

def list_filters(chat_id: int):
    with closing(conn.cursor()) as cur:
        cur.execute('SELECT keyword FROM filters WHERE chat_id=?', (chat_id,))
        return [r[0] for r in cur.fetchall()]

def clear_filters(chat_id: int) -> None:
    with closing(conn.cursor()) as cur:
        cur.execute('DELETE FROM filters WHERE chat_id=?', (chat_id,))
        conn.commit()

# -- CONNECTION ACCESSOR --

def get_conn():
    return conn

# --- Async helper functions used by some handlers ---

async def get_setting(chat_id: int, key: str, default=None):
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            "SELECT value FROM settings WHERE chat_id=? AND key=?",
            (chat_id, key),
        )
        row = await cur.fetchone()
        return row[0] if row else default


async def increment_warning(chat_id: int, user_id: int) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "CREATE TABLE IF NOT EXISTS warnings (chat_id INTEGER, user_id INTEGER, count INTEGER DEFAULT 0, PRIMARY KEY(chat_id, user_id))"
        )
        cur = await db.execute(
            "SELECT count FROM warnings WHERE chat_id=? AND user_id=?",
            (chat_id, user_id),
        )
        row = await cur.fetchone()
        count = row[0] + 1 if row else 1
        await db.execute(
            "REPLACE INTO warnings(chat_id, user_id, count) VALUES (?,?,?)",
            (chat_id, user_id, count),
        )
        await db.commit()
        return count


async def reset_warning(chat_id: int, user_id: int) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "DELETE FROM warnings WHERE chat_id=? AND user_id=?",
            (chat_id, user_id),
        )
        await db.commit()


async def is_approved(chat_id: int, user_id: int) -> bool:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "CREATE TABLE IF NOT EXISTS approvals (chat_id INTEGER, user_id INTEGER, PRIMARY KEY(chat_id, user_id))"
        )
        cur = await db.execute(
            "SELECT 1 FROM approvals WHERE chat_id=? AND user_id=?",
            (chat_id, user_id),
        )
        row = await cur.fetchone()
        return bool(row)


async def get_approval_mode(chat_id: int) -> bool:
    # stored in settings table as approval_mode=on|off
    val = await get_setting(chat_id, "approval_mode", "off")
    return str(val) == "on"


async def get_bio_filter(chat_id: int) -> bool:
    val = await get_setting(chat_id, "biofilter", "off")
    return str(val) == "on"


async def get_admins(chat_id: int) -> list[int]:
    async with aiosqlite.connect(DB_PATH) as db:
        rows = await db.execute_fetchall(
            "SELECT user_id FROM approvals WHERE chat_id=?",
            (chat_id,),
        )
        return [r[0] for r in rows]


async def export_chat_data(chat_id: int) -> dict:
    async with aiosqlite.connect(DB_PATH) as db:
        data = {}
        data["filters"] = await db.execute_fetchall(
            "SELECT keyword, response FROM filters WHERE chat_id=?",
            (chat_id,),
        )
        data["notes"] = await db.execute_fetchall(
            "SELECT name, content FROM notes WHERE chat_id=?",
            (chat_id,),
        )
        data["settings"] = await db.execute_fetchall(
            "SELECT key, value FROM settings WHERE chat_id=?",
            (chat_id,),
        )
        data["warnings"] = await db.execute_fetchall(
            "SELECT user_id, count FROM warnings WHERE chat_id=?",
            (chat_id,),
        )
        return {
            "filters": [{"keyword": k, "response": r} for k, r in data["filters"]],
            "notes": [{"name": n, "content": c} for n, c in data["notes"]],
            "settings": {k: v for k, v in data["settings"]},
            "warnings": {u: c for u, c in data["warnings"]},
        }


async def import_chat_data(chat_id: int, data: dict) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        count = 0
        for item in data.get("filters", []):
            await db.execute(
                "REPLACE INTO filters(chat_id, keyword, response) VALUES(?,?,?)",
                (chat_id, item["keyword"].lower(), item["response"]),
            )
            count += 1
        for item in data.get("notes", []):
            await db.execute(
                "REPLACE INTO notes(chat_id, name, content) VALUES(?,?,?)",
                (chat_id, item["name"].lower(), item["content"]),
            )
            count += 1
        for key, value in data.get("settings", {}).items():
            await db.execute(
                "REPLACE INTO settings(chat_id, key, value) VALUES(?,?,?)",
                (chat_id, key, value),
            )
        for user_id, warn_count in data.get("warnings", {}).items():
            await db.execute(
                "REPLACE INTO warnings(chat_id, user_id, count) VALUES(?,?,?)",
                (chat_id, int(user_id), int(warn_count)),
            )
        await db.commit()
        return count
