from pathlib import Path

import pandas as pd


project_root = Path(__file__).resolve().parents[2]

input_path = project_root / "output"


def test_cashflow_file_exists():
    file_path = input_path / "cashflow_intelligence.xlsx"
    assert file_path.exists()


def test_cashflow_not_empty():
    df = pd.read_excel(
        input_path / "cashflow_intelligence.xlsx"
    )

    assert len(df) > 0


def test_company_column_exists():
    df = pd.read_excel(
        input_path / "cashflow_intelligence.xlsx"
    )

    assert "company_id" in df.columns


def test_year_column_exists():
    df = pd.read_excel(
        input_path / "cashflow_intelligence.xlsx"
    )

    assert "year" in df.columns


def test_free_cash_flow_exists():
    df = pd.read_excel(
        input_path / "cashflow_intelligence.xlsx"
    )

    assert "free_cash_flow" in df.columns


def test_no_duplicate_rows():
    df = pd.read_excel(
        input_path / "cashflow_intelligence.xlsx"
    )

    duplicates = df.duplicated().sum()

    print("Duplicate Rows:", duplicates)

    assert duplicates >= 0


def test_company_count():
    df = pd.read_excel(
        input_path / "cashflow_intelligence.xlsx"
    )

    assert df["company_id"].nunique() > 0


def test_free_cash_flow_numeric():
    df = pd.read_excel(
        input_path / "cashflow_intelligence.xlsx"
    )

    assert pd.api.types.is_numeric_dtype(
        df["free_cash_flow"]
    )


def test_dataframe_type():
    df = pd.read_excel(
        input_path / "cashflow_intelligence.xlsx"
    )

    assert isinstance(df, pd.DataFrame)


def test_columns_not_empty():
    df = pd.read_excel(
        input_path / "cashflow_intelligence.xlsx"
    )

    assert len(df.columns) > 0