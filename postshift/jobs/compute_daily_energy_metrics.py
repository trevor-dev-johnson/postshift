import sqlite3
import json
from collections import Counter
from datetime import datetime

from postshift.storage.derived_schema import initialize_derived_schema


DB_PATH = "postshift.db"

def extract_energy_events(conn: sqlite3.Connection):
  cursor = conn.cursor()
  rows = cursor.execute(
  """
  SELECT timestamp, payload
  FROM events
  WHERE event_type = 'energy_assessed'
  """
  ).fetchall()
  
  for timestamp, payload in rows:
    data = json.loads(payload)
    date = timestamp.split("T")[0]
    yield date, data["energy"]
    
def compute_daily_metrics(events):
  grouped = {}
  
  for date, energy in events:
    grouped.setdefault(date, []).append(energy)
    
  
  for date, energies, in grouped.items():
    counts = Counter(energies)
    yield {
      "date": date,
      "assessments_count": len(energies),
      "dead_count": counts.get("dead", 0),
      "low_count": counts.get("low", 0),
      "normal_count": counts.get("normal", 0),
      "sharp_count": counts.get("sharp", 0),
    }
    
def load_daily_metrics(conn: sqlite3.Connection, metrics):
  cursor = conn.cursor()
  
  for row in metrics:
    cursor.execute(
      """
        INSERT OR REPLACE INTO daily_energy_metrics (
          date,
          assessments_count,
          dead_count,
          low_count,
          normal_count,
          sharp_count
      )
      VALUES (?, ?, ?, ?, ?, ?)
      """,
      (
          row["date"],
          row["assessments_count"],
          row["dead_count"],
          row["low_count"],
          row["normal_count"],
          row["sharp_count"],
      ),
    )
    
  conn.commit()
  
def main():
  conn = sqlite3.connect(DB_PATH)
  
  initialize_derived_schema(conn)
  
  events = extract_energy_events(conn)
  metrics = compute_daily_metrics(events)
  load_daily_metrics(conn, metrics)
  
  print("Daily energy metrics computed.")
  
if __name__ == "__main__":
  main()