from pathlib import Path
import sqlite3

from fastapi import APIRouter, Query

router = APIRouter()

project_root = Path(__file__).resolve().parents[3]

db_path = project_root / "db" / "nifty100.db"


def get_connection():
    return sqlite3.connect(db_path)


@router.get("/screener")
def screener(
    sector: str = Query(None),
    min_pe: float = Query(None),
    max_pe: float = Query(None),
    min_pb: float = Query(None),
    max_pb: float = Query(None),
    min_fcf: float = Query(None),
    max_fcf: float = Query(None),
    limit: int = 100,
):

    conn = get_connection()

    query = """
    SELECT
        company_id,
        year,
        pe_ratio,
        pb_ratio,
        fcf_yield_pct,
        market_cap_crore,
        valuation_flag,
        broad_sector
    FROM valuation_summary
    WHERE 1=1
    """

    params = []

    if sector:
        query += " AND broad_sector=?"
        params.append(sector)

    if min_pe is not None:
        query += " AND pe_ratio>=?"
        params.append(min_pe)

    if max_pe is not None:
        query += " AND pe_ratio<=?"
        params.append(max_pe)

    if min_pb is not None:
        query += " AND pb_ratio>=?"
        params.append(min_pb)

    if max_pb is not None:
        query += " AND pb_ratio<=?"
        params.append(max_pb)

    if min_fcf is not None:
        query += " AND fcf_yield_pct>=?"
        params.append(min_fcf)

    if max_fcf is not None:
        query += " AND fcf_yield_pct<=?"
        params.append(max_fcf)

    query += " ORDER BY company_id LIMIT ?"
    params.append(limit)

    cursor = conn.execute(query, params)

    columns = [c[0] for c in cursor.description]

    rows = cursor.fetchall()

    conn.close()

    result = []

    for row in rows:
        result.append(dict(zip(columns, row)))

    return {"count": len(result), "companies": result}
