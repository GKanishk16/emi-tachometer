-- EMI Tachometer | Author: Kanishk Gupta
-- Q1: Portfolio default rate plus default rate by LTV band.
WITH totals AS (
    SELECT 'Portfolio' AS view_label, COUNT(*) AS loan_count,
           SUM(loan_default) AS defaults,
           AVG(loan_default::DOUBLE) AS default_rate
    FROM fact_loans
), bands AS (
    SELECT ltv_band AS view_label, COUNT(*) AS loan_count,
           SUM(loan_default) AS defaults,
           AVG(loan_default::DOUBLE) AS default_rate
    FROM fact_loans
    GROUP BY ltv_band
)
SELECT * FROM totals
UNION ALL
SELECT * FROM bands
ORDER BY view_label; 
-- Alternate: GROUPING SETS on ltv_band can emit the total and bands in one aggregation.
