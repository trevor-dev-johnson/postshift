import sqlite3
import json
from typing import List

from postshift.storage.red_zone_schema import initialize_red_zone_schema
from postshift.storage.local import EventStore

DB_PATH = "postshift.db"

DEAD_LOW_RATIO_THRESHOLD = 0.6
RED_ZONE_DAYS_THRESHOLD = 3
RECOVERY_SCORE_THRESHOLD = 40.0

def fetch_weekly_metrics(conn: sqlite3.Connection):
    cursor = conn.cursor()
    rows = cursor.execute(
        """
        SELECT
            end_date,
            dead_low_ratio,
            red_zone_days,
            recovery_score
        FROM weekly_recovery_metrics
        ORDER BY end_date
        """
    ).fetchall()

    return [
        {
            "end_date": end_date,
            "dead_low_ratio": dead_low_ratio,
            "red_zone_days": red_zone_days,
            "recovery_score": recovery_score,
        }
        for end_date, dead_low_ratio, red_zone_days, recovery_score in rows
    ]
    
def evaluate_red_zone(row) -> (int, List[str]):
    reasons = []

    if row["dead_low_ratio"] >= DEAD_LOW_RATIO_THRESHOLD:
        reasons.append("dead_low_ratio")

    if row["red_zone_days"] >= RED_ZONE_DAYS_THRESHOLD:
        reasons.append("red_zone_days")

    if row["recovery_score"] <= RECOVERY_SCORE_THRESHOLD:
        reasons.append("recovery_score")

    triggered = 1 if reasons else 0
    return triggered, reasons
  
def load_red_zone_alerts(conn: sqlite3.Connection, alerts):
    cursor = conn.cursor()

    for a in alerts:
        cursor.execute(
            """
            INSERT OR REPLACE INTO red_zone_alerts (
                end_date,
                dead_low_ratio,
                red_zone_days,
                recovery_score,
                triggered
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                a["end_date"],
                a["dead_low_ratio"],
                a["red_zone_days"],
                a["recovery_score"],
                a["triggered"],
            ),
        )

    conn.commit()
    
def emit_events(alerts):
    store = EventStore()

    for a in alerts:
        if a["triggered"]:
            store.log_event(
                event_type="red_zone_detected",
                payload={
                    "end_date": a["end_date"],
                    "dead_low_ratio": a["dead_low_ratio"],
                    "red_zone_days": a["red_zone_days"],
                    "recovery_score": a["recovery_score"],
                    "reasons": a["reasons"],
                },
            )
            

def main():
    conn = sqlite3.connect(DB_PATH)

    initialize_red_zone_schema(conn)

    weekly = fetch_weekly_metrics(conn)

    alerts = []
    for row in weekly:
        triggered, reasons = evaluate_red_zone(row)
        alerts.append(
            {
                "end_date": row["end_date"],
                "dead_low_ratio": row["dead_low_ratio"],
                "red_zone_days": row["red_zone_days"],
                "recovery_score": row["recovery_score"],
                "triggered": triggered,
                "reasons": reasons,
            }
        )

    load_red_zone_alerts(conn, alerts)
    emit_events(alerts)

    print("Red-zone detection completed.")


if __name__ == "__main__":
    main()