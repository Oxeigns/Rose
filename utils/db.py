import sqlite3
from contextlib import closing

DB_PATH = 'rose.db'

conn = sqlite3.connect(DB_PATH, check_same_thread=False)

with closing(conn.cursor()) as cur:
    cur.execute('''CREATE TABLE IF NOT EXISTS warnings(
        user_id INTEGER,
        chat_id INTEGER,
        warn_count INTEGER DEFAULT 0,
        timestamp INTEGER
    )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS notes(
        chat_id INTEGER,
        name TEXT,
        content TEXT
    )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS settings(
        chat_id INTEGER,
        key TEXT,
        value TEXT,
        PRIMARY KEY(chat_id, key)
    )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS filters(
        chat_id INTEGER,
        keyword TEXT,
        response TEXT,
        PRIMARY KEY(chat_id, keyword)
    )''')
    conn.commit()

def get_conn():
    return conn

def set_chat_setting(chat_id: int, key: str, value: str) -> None:
    with closing(conn.cursor()) as cur:
        cur.execute(
            'REPLACE INTO settings (chat_id, key, value) VALUES (?,?,?)',
            (chat_id, key, value),
        )
        conn.commit()


def get_chat_setting(chat_id: int, key: str, default=None):
    with closing(conn.cursor()) as cur:
        cur.execute(
            'SELECT value FROM settings WHERE chat_id=? AND key=?',
            (chat_id, key),
        )
        row = cur.fetchone()
    return row[0] if row else default


def add_filter(chat_id: int, keyword: str, response: str) -> None:
    with closing(conn.cursor()) as cur:
        cur.execute(
            'REPLACE INTO filters (chat_id, keyword, response) VALUES (?,?,?)',
            (chat_id, keyword.lower(), response),
        )
        conn.commit()


def remove_filter(chat_id: int, keyword: str) -> None:
    with closing(conn.cursor()) as cur:
        cur.execute(
            'DELETE FROM filters WHERE chat_id=? AND keyword=?',
            (chat_id, keyword.lower()),
        )
        conn.commit()


def get_filter(chat_id: int, keyword: str):
    with closing(conn.cursor()) as cur:
        cur.execute(
            'SELECT response FROM filters WHERE chat_id=? AND keyword=?',
            (chat_id, keyword.lower()),
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
