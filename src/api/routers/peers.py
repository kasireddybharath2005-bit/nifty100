from pathlib import Path
import sqlite3

from fastapi import APIRouter, HTTPException

router = APIRouter()

project_root = Path(__file__).resolve().parents[3]

db_path = project_root / "db" / "nifty100.db"


def get_connection():
    return sqlite3.connect(db_path)


# -------------------------------------------------
# GET ALL COMPANIES IN A PEER GROUP
# -------------------------------------------------


@router.get("/peers/{group_name}")
def get_peer_group(group_name: str):

    conn = get_connection()

    query = """
    SELECT
        company_id,
        peer_group,
        roe_percentile,
        roce_percentile,
        pe_percentile,
        pb_percentile,
        market_cap_percentile
    FROM peer_percentiles
    WHERE peer_group=?
    ORDER BY company_id
    """

    cursor = conn.execute(query, (group_name,))

    columns = [col[0] for col in cursor.description]

    rows = cursor.fetchall()

    conn.close()

    if len(rows) == 0:
        raise HTTPException(status_code=404, detail="Peer group not found")

    result = []

    for row in rows:
        result.append(dict(zip(columns, row)))

    return {"peer_group": group_name, "count": len(result), "companies": result}


# -------------------------------------------------
# COMPARE A COMPANY WITH ITS PEER GROUP
# -------------------------------------------------


@router.get("/companies/{ticker}/peers/compare")
def compare_company(ticker: str):

    conn = get_connection()

    query = """
    SELECT *
    FROM peer_percentiles
    WHERE company_id=?
    """

    cursor = conn.execute(query, (ticker.upper(),))

    columns = [col[0] for col in cursor.description]

    row = cursor.fetchone()

    conn.close()

    if row is None:
        raise HTTPException(status_code=404, detail="Company not found")

    return dict(zip(columns, row))
