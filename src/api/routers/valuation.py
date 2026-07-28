from pathlib import Path
import sqlite3

from fastapi import APIRouter, HTTPException

router = APIRouter()

# --------------------------------------------------
# DATABASE
# --------------------------------------------------

project_root = Path(__file__).resolve().parents[3]

db_path = project_root / "db" / "nifty100.db"


def get_connection():
    return sqlite3.connect(db_path)


# --------------------------------------------------
# GET ALL VALUATION DATA
# --------------------------------------------------


@router.get("/valuation")
def get_all_valuation():

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
        dividend_yield_pct,
        fcf_yield_pct,
        broad_sector,
        valuation_flag
    FROM valuation_summary
    ORDER BY company_id
    """

    cursor = conn.execute(query)

    columns = [col[0] for col in cursor.description]

    rows = cursor.fetchall()

    conn.close()

    data = []

    for row in rows:
        data.append(dict(zip(columns, row)))

    return {"count": len(data), "valuation": data}


# --------------------------------------------------
# GET SINGLE COMPANY VALUATION
# --------------------------------------------------


@router.get("/valuation/{ticker}")
def get_company_valuation(ticker: str):

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
        dividend_yield_pct,
        fcf_yield_pct,
        broad_sector,
        valuation_flag
    FROM valuation_summary
    WHERE company_id=?
    """

    cursor = conn.execute(query, (ticker.upper(),))

    columns = [col[0] for col in cursor.description]

    row = cursor.fetchone()

    conn.close()

    if row is None:

        raise HTTPException(status_code=404, detail="Company not found")

    return dict(zip(columns, row))


# --------------------------------------------------
# FILTER BY SECTOR
# --------------------------------------------------


@router.get("/valuation/sector/{sector}")
def valuation_by_sector(sector: str):

    conn = get_connection()

    query = """
    SELECT
        company_id,
        pe_ratio,
        pb_ratio,
        ev_ebitda,
        dividend_yield_pct,
        valuation_flag
    FROM valuation_summary
    WHERE broad_sector=?
    ORDER BY company_id
    """

    cursor = conn.execute(query, (sector,))

    columns = [col[0] for col in cursor.description]

    rows = cursor.fetchall()

    conn.close()

    result = []

    for row in rows:
        result.append(dict(zip(columns, row)))

    return {"sector": sector, "count": len(result), "companies": result}
