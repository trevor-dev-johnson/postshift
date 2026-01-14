import sqlite3
from datetime import datetime, timedelta

from postshift.storage.weekly_schema import initialize_weekly_schema


DB_PATH = "postshift.db"


def fetch_daily_metrics(conn: sqlite3.Connection):
    cursor = conn.cursor()
    rows = cursor.execute(
        """
        SELECT
            date,
            assessments_count,
            dead_count,
            low_count
        FROM daily_energy_metrics
        ORDER BY date
        """
    ).fetchall()
    
    return [
      {
        "date": datetime.fromisoformat(date),
        "assessments": assessments,
        "dead": dead,
        "low": low,
      }
      for date, assessments, dead, low in rows
    ]
    
def compute_weekly_metrics(daily_rows):
  results = []
  
  for i, row in enumerate(daily_rows):
    window = daily_rows[max(0, i - 6) : i + 1]
    
    total_assessments = sum(d["assessments"] for d in window)
    total_dead = sum(d["dead"] for d in window)
    total_low = sum(d["low"] for d in window)
    
    dead_low_ratio = (
      (total_dead + total_low) / total_assessments
      if total_assessments > 0
      else 0.0
    )
    
    red_zone_days = sum(1 for d in window if d["dead"] > 0)
    
    recovery_score = round(
      max(0.0, 100.0 * (1.0 - dead_low_ratio)), 2
    )
    
    results.append(
        {
            "end_date": row["date"].date().isoformat(),
            "assessments_count": total_assessments,
            "dead_low_ratio": round(dead_low_ratio, 3),
            "red_zone_days": red_zone_days,
            "recovery_score": recovery_score,
        }
    )

  return results

def load_weekly_metrics(conn: sqlite3.Connection, metrics):
    cursor = conn.cursor()

    for row in metrics:
        cursor.execute(
            """
            INSERT OR REPLACE INTO weekly_recovery_metrics (
                end_date,
                assessments_count,
                dead_low_ratio,
                red_zone_days,
                recovery_score
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                row["end_date"],
                row["assessments_count"],
                row["dead_low_ratio"],
                row["red_zone_days"],
                row["recovery_score"],
            ),
        )

    conn.commit()
    
def main():
  conn = sqlite3.connect(DB_PATH)
  
  initialize_weekly_schema(conn)
  
  daily_rows = fetch_daily_metrics(conn)
  weekly_metrics = compute_weekly_metrics(daily_rows)
  load_weekly_metrics(conn, weekly_metrics)

  print("Weekly recovery metrics computed.")


if __name__ == "__main__":
    main()