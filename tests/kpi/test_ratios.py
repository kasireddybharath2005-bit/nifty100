import pytest


def calculate_roe(net_profit, equity):
    if equity <= 0:
        return None
    return round((net_profit / equity) * 100, 2)


def calculate_debt_equity(debt, equity):
    if equity == 0:
        return None
    return round(debt / equity, 2)


def calculate_icr(ebit, interest):
    if interest == 0:
        return None
    return round(ebit / interest, 2)


def calculate_opm(op_profit, revenue):
    if revenue == 0:
        return None
    return round((op_profit / revenue) * 100, 2)


def calculate_cagr(start, end, years):
    if start <= 0 or years <= 0:
        return None
    return round(((end / start) ** (1 / years) - 1) * 100, 2)


def calculate_cfo_quality(cfo, net_profit):
    if net_profit == 0:
        return None
    return round(cfo / net_profit, 2)


# ----------------------
# ROE Tests
# ----------------------

def test_roe_positive():
    assert calculate_roe(100, 500) == 20.00


def test_roe_negative_equity():
    assert calculate_roe(100, -10) is None


# ----------------------
# Debt Equity Tests
# ----------------------

def test_de_ratio():
    assert calculate_debt_equity(200, 100) == 2.00


def test_de_zero_equity():
    assert calculate_debt_equity(100, 0) is None


# ----------------------
# Interest Coverage Tests
# ----------------------

def test_icr():
    assert calculate_icr(500, 50) == 10.00


def test_icr_zero_interest():
    assert calculate_icr(500, 0) is None


# ----------------------
# OPM Tests
# ----------------------

def test_opm():
    assert calculate_opm(250, 1000) == 25.00


# ----------------------
# CAGR Tests
# ----------------------

def test_cagr():
    assert calculate_cagr(100, 200, 5) == 14.87


# ----------------------
# CFO Quality Tests
# ----------------------

def test_cfo_quality():
    assert calculate_cfo_quality(500, 400) == 1.25


def test_cfo_zero_profit():
    assert calculate_cfo_quality(500, 0) is None