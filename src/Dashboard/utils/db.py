print("=" * 60)
print("LOADED DB.PY")
print(__file__)
print("=" * 60)
import sqlite3
import pandas as pd
from pathlib import Path

project_root = Path(__file__).resolve().parents[3]

db_path = project_root / "db" / "nifty100.db"


def get_connection():
    return sqlite3.connect(db_path)


def get_companies():

    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT DISTINCT company_id
        FROM financial_ratios
        ORDER BY company_id
        """,
        conn
    )

    conn.close()

    return df


def get_ratios(company):

    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT *
        FROM financial_ratios
        WHERE company_id=?
        ORDER BY year
        """,
        conn,
        params=[company]
    )

    conn.close()

    return df

def get_pl(company):

    print(">>> NEW get_pl() is running")
    print(">>> db.py path:", __file__)

    conn = get_connection()

    query = """
    SELECT *
    FROM profitandloss
    WHERE company_id=?
    ORDER BY year
    """

    print(query)

    df = pd.read_sql(
        query,
        conn,
        params=[company]
    )

    conn.close()

    return df
def get_bs(company):

    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT *
        FROM balancesheet
        WHERE company_id=?
        ORDER BY year
        """,
        conn,
        params=[company]
    )

    conn.close()

    return df


def get_cf(company):

    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT *
        FROM cashflow
        WHERE company_id=?
        ORDER BY year
        """,
        conn,
        params=[company]
    )

    conn.close()

    return df
def get_screener_data():

    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT
            company_id,
            roe_calculated,
            debt_to_equity,
            net_profit_margin,
            operating_profit_margin,
            asset_turnover,
            revenue_cagr_5yr,
            profit_cagr_5yr
        FROM financial_ratios
        """,
        conn
    )

    conn.close()

    return df


def get_peer_companies():

    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT DISTINCT
            "HDFCBANK" AS company_id
        FROM peer_groups
        ORDER BY company_id
        """,
        conn
    )

    conn.close()

    return df

def get_trend_data(company):

    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT
            year,
            roe_calculated,
            net_profit_margin,
            revenue_cagr_5yr,
            profit_cagr_5yr
        FROM financial_ratios
        WHERE company_id=?
        ORDER BY year
        """,
        conn,
        params=[company]
    )

    conn.close()

    return df

# -------------------------------------------------------
# Peer Comparison Data
# -------------------------------------------------------

def get_peer_data(company):

    conn = get_connection()

    # Get the selected company's peer group
    peer_group_query = """
    SELECT peer_group_name
    FROM peer_groups
    WHERE company_id = ?
    LIMIT 1
    """

    peer_group_df = pd.read_sql(
        peer_group_query,
        conn,
        params=[company]
    )

    if peer_group_df.empty:
        conn.close()
        return pd.DataFrame()

    peer_group = peer_group_df.iloc[0]["peer_group_name"]

    # Get all companies in the same peer group
    query = """
    SELECT
        f.company_id,
        p.peer_group_name,
        f.roe_calculated,
        f.debt_to_equity,
        f.net_profit_margin,
        f.operating_profit_margin,
        f.asset_turnover,
        f.revenue_cagr_5yr,
        f.profit_cagr_5yr
    FROM financial_ratios f
    INNER JOIN peer_groups p
        ON f.company_id = p.company_id
    WHERE p.peer_group_name = ?
    ORDER BY f.roe_calculated DESC
    """

    peer_df = pd.read_sql(
        query,
        conn,
        params=[peer_group]
    )

    conn.close()

    return peer_df

def get_trend_data(company):

    conn = get_connection()

    query = """
    SELECT
        year,
        roe_calculated,
        net_profit_margin,
        operating_profit_margin,
        asset_turnover,
        debt_to_equity,
        revenue_cagr_5yr,
        profit_cagr_5yr
    FROM financial_ratios
    WHERE company_id = ?
    ORDER BY year
    """

    df = pd.read_sql(query, conn, params=[company])

    conn.close()

    return df
def get_sector_data():

    conn = get_connection()

    query = """
    SELECT
        sector_name,
        COUNT(company_id) AS total_companies
    FROM sectors
    GROUP BY sector_name
    ORDER BY total_companies DESC
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df

def get_capital_data(company):

    conn = get_connection()

    query = """
    SELECT
        year,
        equity_capital,
        reserves,
        borrowings,
        total_liabilities,
        total_assets
    FROM balancesheet
    WHERE company_id=?
    ORDER BY year
    """

    df = pd.read_sql(
        query,
        conn,
        params=[company]
    )

    conn.close()

    return df

def get_company_report(company):

    conn = get_connection()

    ratios = pd.read_sql(
        "SELECT * FROM financial_ratios WHERE company_id=?",
        conn,
        params=[company]
    )

    pl = pd.read_sql(
        "SELECT * FROM profitandloss WHERE company_id=?",
        conn,
        params=[company]
    )

    bs = pd.read_sql(
        "SELECT * FROM balancesheet WHERE company_id=?",
        conn,
        params=[company]
    )

    cf = pd.read_sql(
        "SELECT * FROM cashflow WHERE company_id=?",
        conn,
        params=[company]
    )

    conn.close()

    return ratios, pl, bs, cf