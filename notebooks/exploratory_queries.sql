SELECT COUNT(*) AS total_companies
FROM companies;
SELECT company_name, roce_percentage
FROM companies
ORDER BY roce_percentage DESC
LIMIT 10;
SELECT company_id, roe
FROM analysis
ORDER BY roe DESC
LIMIT 10;
SELECT company_id,
       SUM(net_cash_flow) AS total_cashflow
FROM cashflow
GROUP BY company_id
ORDER BY total_cashflow DESC
LIMIT 10;
SELECT company_id,
       MAX(borrowings) AS borrowings
FROM balancesheet
GROUP BY company_id
ORDER BY borrowings DESC
LIMIT 10;
SELECT AVG(roe)
FROM analysis;
SELECT AVG(roce_percentage)
FROM companies;
SELECT SUM(market_cap)
FROM market_cap;
SELECT DISTINCT company_id
FROM cashflow
WHERE net_cash_flow > 0;
SELECT 'companies', COUNT(*) FROM companies
UNION ALL
SELECT 'analysis', COUNT(*) FROM analysis
UNION ALL
SELECT 'balancesheet', COUNT(*) FROM balancesheet
UNION ALL
SELECT 'cashflow', COUNT(*) FROM cashflow;