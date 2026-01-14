import sqlite3

RED_ZONE_SCHEMA = """
CREATE TABLE IF NOT EXISTS red_zone_alerts (
    end_date TEXT PRIMARY KEY,
    dead_low_ratio REAL NOT NULL,
    red_zone_days INTEGER NOT NULL,
    recovery_score REAL NOT NULL,
    triggered INTEGER NOT NULL
);
"""

def initialize_red_zone_schema(conn: sqlite3.Connection) -> None:
    cursor = conn.cursor()
    cursor.execute(RED_ZONE_SCHEMA)
    conn.commit()
