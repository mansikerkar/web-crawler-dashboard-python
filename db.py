import sqlite3
import os

DB_PATH = "data/crawl.db"

def init_db():
    os.makedirs("data", exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS pages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            title TEXT,
            text TEXT
        )
    """)

    conn.commit()
    conn.close()

def insert_pages(pages):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    for p in pages:
        cur.execute(
            "INSERT INTO pages (url, title, text) VALUES (?, ?, ?)",
            (p["url"], p["title"], p["text"])
        )

    conn.commit()
    conn.close()

def fetch_pages():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    rows = cur.execute(
        "SELECT url, title, text FROM pages ORDER BY id DESC"
    ).fetchall()

    conn.close()
    return rows
