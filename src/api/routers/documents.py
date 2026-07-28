from pathlib import Path
import sqlite3

from fastapi import APIRouter, HTTPException

router = APIRouter()

project_root = Path(__file__).resolve().parents[3]

db_path = project_root / "db" / "nifty100.db"


def get_connection():
    return sqlite3.connect(db_path)


@router.get("/companies/{ticker}/documents")
def company_documents(ticker: str):

    conn = get_connection()

    query = """
    SELECT
        company_id,
        document_type,
        document_name,
        document_url
    FROM documents
    WHERE company_id=?
    ORDER BY document_type
    """

    cursor = conn.execute(query, (ticker.upper(),))

    columns = [col[0] for col in cursor.description]

    rows = cursor.fetchall()

    conn.close()

    if len(rows) == 0:
        raise HTTPException(
            status_code=404,
            detail="No documents found"
        )

    result = []

    for row in rows:
        result.append(dict(zip(columns, row)))

    return {
        "company": ticker.upper(),
        "documents": result
    }