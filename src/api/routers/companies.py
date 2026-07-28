from pathlib import Path
import sqlite3
from fastapi import APIRouter, HTTPException

router = APIRouter()

project_root = Path(__file__).resolve().parents[3]
db_path = project_root / "db" / "nifty100.db"


def get_connection():
    return sqlite3.connect(db_path)


# ------------------------------------------
# GET ALL COMPANIES
# ------------------------------------------

@router.get("/companies")
def get_companies():

    conn = get_connection()

    query = """
    SELECT *
    FROM companies
    ORDER BY company_id
    """

    cursor = conn.execute(query)

    columns = [col[0] for col in cursor.description]

    rows = cursor.fetchall()

    conn.close()

    result = []

    for row in rows:
        result.append(dict(zip(columns, row)))

    return {
        "count": len(result),
        "companies": result
    }


# ------------------------------------------
# GET SINGLE COMPANY
# ------------------------------------------

@router.get("/companies/{ticker}")
def get_company(ticker: str):

    conn = get_connection()

    query = """
    SELECT *
    FROM companies
    WHERE company_id=?
    """

    cursor = conn.execute(query, (ticker.upper(),))

    columns = [col[0] for col in cursor.description]

    row = cursor.fetchone()

    conn.close()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    return dict(zip(columns, row))