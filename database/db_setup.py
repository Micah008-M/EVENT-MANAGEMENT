import sqlite3
from utils.constants import DB_FILE

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        date TEXT NOT NULL,
        venue TEXT,
        description TEXT
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS admins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

def seed_users():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    students = [
        ('neha', 'one'), ('daniya', 'two'), ('micah', 'three'),
        ('gauri', 'four'), ('sona', 'five'), ('antony', 'six'),
        ('varghese', 'seven'), ('tiya', 'eight'), ('naina','nine'),
        ('thomas','ten'),
    ]
    cur.executemany("INSERT OR IGNORE INTO students (username, password) VALUES (?, ?)", students)

    admins = [
        ('rinu', 'rinu123'), ('kavitha','kavitha123'),
        ('divya','divya123'), ('priya','priya123'), ('vinodhini','vinodhini123')
    ]
    cur.executemany("INSERT OR IGNORE INTO admins (username, password) VALUES (?, ?)", admins)
    conn.commit()
    conn.close()
