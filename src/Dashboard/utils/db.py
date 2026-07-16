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

    query = """
    SELECT
        company_id,
        return_on_equity_pct,
        debt_to_equity,
        net_profit_margin_pct,
        operating_profit_margin_pct,
        asset_turnover,
        revenue_cagr_5yr,
        profit_cagr_5yr
    FROM financial_ratios
    """

    df = pd.read_sql(query, conn)

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

    query = """
    SELECT
        year,
        return_on_equity_pct,
        net_profit_margin_pct,
        operating_profit_margin_pct,
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
        SELECT
    f.company_id,
    p.peer_group_name,
    f.return_on_equity_pct,
    f.debt_to_equity,
    f.net_profit_margin_pct,
    f.operating_profit_margin_pct,
    f.asset_turnover,
    f.revenue_cagr_5yr,
    f.profit_cagr_5yr
    FROM financial_ratios f
    INNER JOIN peer_groups p
        ON f.company_id = p.company_id
    WHERE p.peer_group_name = ?
    ORDER BY f.return_on_equity_pct DESC
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

def get_home_kpis(year):

    conn = get_connection()

    query = """
    SELECT
        ROUND(AVG(roe_calculated),2) AS avg_roe,
        ROUND(AVG(debt_to_equity),2) AS avg_de,
        ROUND(AVG(asset_turnover),2) AS avg_asset_turnover,
        ROUND(AVG(revenue_cagr_5yr),2) AS avg_revenue_cagr,
        ROUND(AVG(eps_cagr_3yr),2) AS avg_eps_growth,
        COUNT(DISTINCT company_id) AS total_companies,
        SUM(
            CASE
                WHEN debt_to_equity = 0 THEN 1
                ELSE 0
            END
        ) AS debt_free_companies
    FROM financial_ratios
    WHERE year = ?
    """

    df = pd.read_sql(
        query,
        conn,
        params=[year]
    )

    conn.close()

    return df.iloc[0]
def get_sector_distribution():

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

def get_top_companies(year):

    conn = get_connection()

    query = """
    SELECT
        company_id,
        ROUND(AVG(percentile_rank),2) AS composite_score
    FROM peer_percentiles
    WHERE year = ?
    GROUP BY company_id
    ORDER BY composite_score DESC
    LIMIT 5
    """

    df = pd.read_sql(
        query,
        conn,
        params=[year]
    )

    conn.close()

    return df
def get_years():

    conn = get_connection()

    query = """
    SELECT DISTINCT year
    FROM financial_ratios
    ORDER BY year DESC
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df["year"].tolist()

def search_companies(search_text):

    conn = get_connection()

    query = """
    SELECT DISTINCT company_id
    FROM financial_ratios
    WHERE company_id LIKE ?
    ORDER BY company_id
    """

    df = pd.read_sql(
        query,
        conn,
        params=[f"%{search_text}%"]
    )

    conn.close()

    return df

def get_company_info(company):

    conn = get_connection()

    query = """
    SELECT
        company_id,
        sector_name,
        industry,
        market_cap
    FROM sectors
    WHERE company_id = ?
    """

    df = pd.read_sql(
        query,
        conn,
        params=[company]
    )

    conn.close()

    return df

def get_revenue_profit(company):

    conn = get_connection()

    query = """
    SELECT
        year,
        sales,
        net_profit
    FROM profitandloss
    WHERE company_id = ?
    ORDER BY year
    """

    df = pd.read_sql(
        query,
        conn,
        params=[company]
    )

    conn.close()

    return df
def get_roe_asset_turnover(company):

    conn = get_connection()

    query = """
    SELECT
        year,
        roe_calculated,
        asset_turnover
    FROM financial_ratios
    WHERE company_id = ?
    ORDER BY year
    """

    df = pd.read_sql(
        query,
        conn,
        params=[company]
    )

    conn.close()

    return df

def get_screener_filtered(
    roe_min,
    debt_max,
    npm_min,
    opm_min,
    asset_min
):

    conn = get_connection()

    query = """
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
    WHERE
        roe_calculated >= ?
        AND debt_to_equity <= ?
        AND net_profit_margin >= ?
        AND operating_profit_margin >= ?
        AND asset_turnover >= ?
    ORDER BY roe_calculated DESC
    """

    df = pd.read_sql(
        query,
        conn,
        params=[
            roe_min,
            debt_max,
            npm_min,
            opm_min,
            asset_min
        ]
    )

    conn.close()

    return df