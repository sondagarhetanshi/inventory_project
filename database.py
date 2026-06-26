import sqlite3

def create_db():
    conn = sqlite3.connect("inventory.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()


def add_user(username, password):
    conn = sqlite3.connect("inventory.db")
    c = conn.cursor()

    c.execute("INSERT INTO users (username, password) VALUES (?,?)",
              (username, password))

    conn.commit()
    conn.close()


def login_user(username, password):
    conn = sqlite3.connect("inventory.db")
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE username=? AND password=?",
              (username, password))

    result = c.fetchone()
    conn.close()

    return result