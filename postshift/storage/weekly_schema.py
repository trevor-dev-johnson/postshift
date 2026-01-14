import sqlite3

WEEKLY_RECOVERY_SCHEMA = """
CREATE TABLE IF NOT EXISTS weekly_recovery_metrics (
    end_date TEXT PRIMARY KEY,
    assessments_count INTEGER NOT NULL,
    dead_low_ratio REAL NOT NULL,
    red_zone_days INTEGER NOT NULL,
    recovery_score REAL NOT NULL
);
"""

def initialize_weekly_schema(conn: sqlite3.Connection) -> None:
    cursor = conn.cursor()
    cursor.execute(WEEKLY_RECOVERY_SCHEMA)
    conn.commit()
