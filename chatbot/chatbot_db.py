import sqlite3
from datetime import datetime


class Database:
    def __init__(self, db_name="chat_history.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name, timeout=10, check_same_thread=False)
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP )
        """)
        self.conn.commit()

    def store_history(self, role, message):
        cursor = self.conn.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""INSERT INTO history (role, message, timestamp) VALUES (?, ?, ?)""",
                       (role, message, timestamp)
                       )
        self.conn.commit()
        print(f"Stored in database: {self.db_name}, role: {role}, message preview: {message[:20]}...")

    def get_history(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT role, message FROM history ORDER BY timestamp ASC")
        rows = cursor.fetchall()

        history = [{"role": role, "message": message} for role, message in rows]
        return history

    def clear_history(self):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM history")
        self.conn.commit()

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None
