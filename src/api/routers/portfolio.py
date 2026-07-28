from pathlib import Path
import sqlite3

from fastapi import APIRouter

router = APIRouter()

project_root = Path(__file__).resolve().parents[3]

db_path = project_root / "db" / "nifty100.db"


def get_connection():
    return sqlite3.connect(db_path)


@router.get("/portfolio/stats")
def portfolio_statistics():

    conn = get_connection()

    query = """
    SELECT
        ROUND(AVG(pe_ratio),2) AS avg_pe,
        ROUND(AVG(pb_ratio),2) AS avg_pb,
        ROUND(AVG(ev_ebitda),2) AS avg_ev_ebitda,
        ROUND(AVG(dividend_yield_pct),2) AS avg_dividend_yield,
        ROUND(AVG(fcf_yield_pct),2) AS avg_fcf_yield
    FROM valuation_summary
    """

    cursor = conn.execute(query)

    columns = [col[0] for col in cursor.description]

    row = cursor.fetchone()

    conn.close()

    return dict(zip(columns, row))
