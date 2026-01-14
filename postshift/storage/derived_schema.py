import sqlite3

DAILY_ENERGY_SCHEMA = """
CREATE TABLE IF NOT EXISTS daily_energy_metrics (
    date TEXT PRIMARY KEY,
    assessments_count INTEGER NOT NULL,
    dead_count INTEGER NOT NULL,
    low_count INTEGER NOT NULL,
    normal_count INTEGER NOT NULL,
    sharp_count INTEGER NOT NULL
);
"""

def initialize_derived_schema(conn: sqlite3.Connection) -> None:
  cursor = conn.cursor()
  cursor.execute(DAILY_ENERGY_SCHEMA)
  conn.commit()