from pathlib import Path
import sqlite3

from fastapi import APIRouter, HTTPException

router = APIRouter()

project_root = Path(__file__).resolve().parents[3]
db_path = project_root / "db" / "nifty100.db"


def get_connection():
    return sqlite3.connect(db_path)


# ----------------------------------------------------
# GET ALL COMPANIES
# ----------------------------------------------------

@router.get("/companies")
def get_companies():

    conn = get_connection()

    query = """
    SELECT DISTINCT
        company_id
    FROM financial_ratios
    ORDER BY company_id
    """

    companies = conn.execute(query).fetchall()

    conn.close()

    return {
        "count": len(companies),
        "companies": [row[0] for row in companies]
    }


# ----------------------------------------------------
# GET COMPANY PROFILE
# ----------------------------------------------------

@router.get("/companies/{ticker}")
def get_company(ticker: str):

    conn = get_connection()

    query = """
    SELECT *
    FROM financial_ratios
    WHERE company_id=?
    ORDER BY year DESC
    """

    df = conn.execute(query, (ticker.upper(),)).fetchall()

    columns = [
        col[0]
        for col in conn.execute(
            "PRAGMA table_info(financial_ratios)"
        ).fetchall()
    ]

    conn.close()

    if len(df) == 0:

        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    latest = dict(
        zip(columns, df[0])
    )

    return latest