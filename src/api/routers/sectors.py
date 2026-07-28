from pathlib import Path
import sqlite3

from fastapi import APIRouter, HTTPException

router = APIRouter()

project_root = Path(__file__).resolve().parents[3]

db_path = project_root / "db" / "nifty100.db"


def get_connection():
    return sqlite3.connect(db_path)


# -------------------------------------------------
# GET ALL SECTORS
# -------------------------------------------------


@router.get("/sectors")
def get_sectors():

    conn = get_connection()

    query = """
    SELECT
        broad_sector,
        COUNT(DISTINCT company_id) AS company_count,
        ROUND(AVG(pe_ratio),2) AS avg_pe,
        ROUND(AVG(pb_ratio),2) AS avg_pb,
        ROUND(AVG(fcf_yield_pct),2) AS avg_fcf
    FROM valuation_summary
    GROUP BY broad_sector
    ORDER BY broad_sector
    """

    cursor = conn.execute(query)

    columns = [col[0] for col in cursor.description]

    rows = cursor.fetchall()

    conn.close()

    result = []

    for row in rows:
        result.append(dict(zip(columns, row)))

    return {"count": len(result), "sectors": result}


# -------------------------------------------------
# GET COMPANIES BY SECTOR
# -------------------------------------------------


@router.get("/sectors/{sector}/companies")
def companies_by_sector(sector: str):

    conn = get_connection()

    query = """
    SELECT
        company_id,
        year,
        pe_ratio,
        pb_ratio,
        market_cap_crore,
        valuation_flag
    FROM valuation_summary
    WHERE broad_sector=?
    ORDER BY company_id
    """

    cursor = conn.execute(query, (sector,))

    columns = [col[0] for col in cursor.description]

    rows = cursor.fetchall()

    conn.close()

    if len(rows) == 0:
        raise HTTPException(status_code=404, detail="Sector not found")

    companies = []

    for row in rows:
        companies.append(dict(zip(columns, row)))

    return {"sector": sector, "count": len(companies), "companies": companies}
