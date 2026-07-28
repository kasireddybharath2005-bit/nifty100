from pathlib import Path
import sqlite3
import time

from fastapi import APIRouter

router = APIRouter()

project_root = Path(__file__).resolve().parents[3]

db_path = project_root / "db" / "nifty100.db"

start_time = time.time()

# ----------------------------------------------------
# DATABASE CONNECTION
# ----------------------------------------------------

def get_connection():

    return sqlite3.connect(db_path)

# ----------------------------------------------------
# HEALTH CHECK
# ----------------------------------------------------

@router.get("/health")
def health():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table';"
    )

    tables = cursor.fetchall()

    row_counts = {}

    for table in tables:

        table_name = table[0]

        cursor.execute(
            f"SELECT COUNT(*) FROM {table_name}"
        )

        row_counts[table_name] = cursor.fetchone()[0]

    conn.close()

    uptime = round(
        time.time() - start_time,
        2
    )

    return {

        "status": "ok",

        "database": "connected",

        "version": "1.0",

        "uptime_seconds": uptime,

        "tables": row_counts

    }