import sqlite3
from datetime import datetime


class Database:
    def __init__(self, db_name="chat_log.db"):
        self.db_name = db_name
        self.conn = None

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_name, timeout=10)  # remove check_same_thread
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            self.conn = None

    def create_table(self):
        try:
            self.connect()
            if self.conn:
                cursor = self.conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        role TEXT NOT NULL,
                        message TEXT NOT NULL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                self.conn.commit()
        except sqlite3.Error as e:
            print(f"Database table creation error: {e}")

    def store_history(self, role, message):
        try:
            self.connect()
            if self.conn:
                cursor = self.conn.cursor()
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute("""INSERT INTO history (role, message, timestamp) VALUES (?, ?, ?)""",
                               (role, message, timestamp))
                self.conn.commit()
                print(f"Stored in database: {self.db_name}, role: {role}, message preview: {message[:20]}...")
        except sqlite3.Error as e:
            print(f"Database insertion error: {e}")

    def get_history(self):
        try:
            self.connect()
            if self.conn:
                cursor = self.conn.cursor()
                cursor.execute("SELECT role, message FROM history ORDER BY timestamp ASC")
                rows = cursor.fetchall()

                history = []
                for role, message in rows:
                    history.append({
                        "parts": [{"text": message}],
                        "role": role
                    })
                return history
        except sqlite3.Error as e:
            print(f"Database retrieval error: {e}")
            return []

    def clear_history(self):
        try:
            self.connect()
            if self.conn:
                cursor = self.conn.cursor()
                cursor.execute("DELETE FROM history")
                self.conn.commit()
        except sqlite3.Error as e:
            print(f"Database clear error: {e}")

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None
