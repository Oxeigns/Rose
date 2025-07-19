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
