import sqlite3
import json
from datetime import datetime, timezone
from typing import Any

from postshift.storage.schema import initialize_schema

class EventStore:
    def __init__(self, db_path: str = "postshift.db"):
        self.conn = sqlite3.connect(db_path)
        initialize_schema(self.conn)
        
    def log_event(
        self,
        *,
        event_type: str,
        payload: dict[str, Any],
    ) -> None:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO events (event_type, timestamp, payload)
            VALUES (?, ?, ?)
            """,
            (
            event_type,
            datetime.now(timezone.utc).isoformat(),
            json.dumps(payload)
            ),
        )
        self.conn.commit()