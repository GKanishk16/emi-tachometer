-- EMI Tachometer | Author: Kanishk Gupta
-- Q12: Produce a long-format summary suitable for a dashboard table.
WITH portfolio AS (
    SELECT 'Portfolio' AS section, 'All loans' AS category, COUNT(*) AS loan_count,
           SUM(disbursed_amount) AS exposure, SUM(loan_default) AS defaults,
           AVG(loan_default::DOUBLE) AS default_rate
    FROM fact_loans
), segments AS (
    SELECT 'Risk segment', risk_segment, COUNT(*), SUM(disbursed_amount),
           SUM(loan_default), AVG(loan_default::DOUBLE)
    FROM segmented_loans GROUP BY risk_segment
), vintage AS (
    SELECT 'Vintage month', CAST(vintage_month AS VARCHAR), COUNT(*), SUM(disbursed_amount),
           SUM(loan_default), AVG(loan_default::DOUBLE)
    FROM fact_loans GROUP BY vintage_month
), ltv AS (
    SELECT 'LTV band', ltv_band, COUNT(*), SUM(disbursed_amount),
           SUM(loan_default), AVG(loan_default::DOUBLE)
    FROM fact_loans GROUP BY ltv_band
)
SELECT * FROM portfolio UNION ALL SELECT * FROM segments
UNION ALL SELECT * FROM vintage UNION ALL SELECT * FROM ltv
ORDER BY section, category;
-- Alternate: materialize separate aggregate tables for dashboard-specific refresh patterns.
