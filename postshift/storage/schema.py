import sqlite3

EVENTS_SCHEMA = """
CREATE TABLE IF NOT EXISTS events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    payload TEXT NOT NULL
);
"""

def initialize_schema(conn: sqlite3.Connection) -> None:
    cursor = conn.cursor()
    cursor.execute(EVENTS_SCHEMA)
    conn.commit()
