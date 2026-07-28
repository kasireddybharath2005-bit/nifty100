import pandas as pd


def validate_positive(value):
    return value > 0


def validate_not_null(value):
    return pd.notna(value)


def validate_percentage(value):
    return 0 <= value <= 100


# -----------------------
# Positive Value Tests
# -----------------------

def test_positive_pass():
    assert validate_positive(100)


def test_positive_fail():
    assert not validate_positive(-10)


# -----------------------
# Null Tests
# -----------------------

def test_not_null():
    assert validate_not_null(50)


def test_null():
    assert not validate_not_null(None)


# -----------------------
# Percentage Tests
# -----------------------

def test_percentage_valid():
    assert validate_percentage(25)


def test_percentage_zero():
    assert validate_percentage(0)


def test_percentage_hundred():
    assert validate_percentage(100)


def test_percentage_negative():
    assert not validate_percentage(-5)


def test_percentage_above():
    assert not validate_percentage(150)


def test_dataframe_rule():

    df = pd.DataFrame({
        "roe": [15, -2, 30],
        "pe_ratio": [20, 25, None]
    })

    assert df["roe"].min() < 0
    assert df["pe_ratio"].isna().sum() == 1