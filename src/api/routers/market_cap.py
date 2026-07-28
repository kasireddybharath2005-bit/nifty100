from pathlib import Path
import sqlite3

from fastapi import APIRouter, HTTPException

router = APIRouter()

project_root = Path(__file__).resolve().parents[3]

db_path = project_root / "db" / "nifty100.db"


def get_connection():
    return sqlite3.connect(db_path)


# ---------------------------------------------
# MARKET CAP HISTORY
# ---------------------------------------------


@router.get("/market-cap/{ticker}")
def market_cap_history(ticker: str):

    conn = get_connection()

    query = """
    SELECT
        company_id,
        year,
        market_cap_crore,
        enterprise_value_crore,
        pe_ratio,
        pb_ratio,
        ev_ebitda,
        dividend_yield_pct
    FROM valuation_summary
    WHERE company_id=?
    ORDER BY year
    """

    cursor = conn.execute(query, (ticker.upper(),))

    columns = [col[0] for col in cursor.description]

    rows = cursor.fetchall()

    conn.close()

    if len(rows) == 0:
        raise HTTPException(status_code=404, detail="Company not found")

    result = []

    for row in rows:
        result.append(dict(zip(columns, row)))

    return {"company": ticker.upper(), "history": result}
