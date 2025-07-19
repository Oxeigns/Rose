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
