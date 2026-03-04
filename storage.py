import sqlite3
import json
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "runs.db")

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                api_name TEXT,
                timestamp TEXT,
                passed INTEGER,
                failed INTEGER,
                error_rate REAL,
                latency_avg REAL,
                latency_p95 REAL,
                details TEXT
            )
        """)
        conn.commit()

def save_run(run_data):
    init_db()
    
    summary = run_data.get("summary", {})
    details_json = json.dumps(run_data.get("tests", []))
    
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            INSERT INTO runs (
                api_name, timestamp, passed, failed, error_rate,
                latency_avg, latency_p95, details
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            run_data.get("api", "Unknown"),
            run_data.get("timestamp", datetime.now().isoformat()),
            summary.get("passed", 0),
            summary.get("failed", 0),
            summary.get("error_rate", 0.0),
            summary.get("latency_ms_avg", 0.0),
            summary.get("latency_ms_p95", 0.0),
            details_json
        ))
        conn.commit()

def list_runs(limit=10):
    init_db()
    runs = []
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.execute("SELECT * FROM runs ORDER BY id DESC LIMIT ?", (limit,))
        for row in cursor:
            runs.append({
                "id": row["id"],
                "api": row["api_name"],
                "timestamp": row["timestamp"],
                "summary": {
                    "passed": row["passed"],
                    "failed": row["failed"],
                    "error_rate": row["error_rate"],
                    "latency_ms_avg": row["latency_avg"],
                    "latency_ms_p95": row["latency_p95"],
                },
                "tests": json.loads(row["details"])
            })
    return runs

def get_last_run():
    runs = list_runs(limit=1)
    if runs:
        return runs[0]
    return None
