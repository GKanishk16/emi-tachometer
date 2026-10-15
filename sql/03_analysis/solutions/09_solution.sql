-- EMI Tachometer | Author: Kanishk Gupta
-- Q9: Quantify thin/no bureau history and compare default rates.
WITH flagged AS (
    SELECT *,
       CASE WHEN bureau_score = 0 OR bureau_description = 'No Bureau History Available'
              OR credit_history_months IS NULL OR credit_history_months < 6
            THEN 'Thin / no history' ELSE 'Established history' END AS bureau_history_group
    FROM fact_loans
), totals AS (
    SELECT COUNT(*) AS portfolio_loans FROM flagged
)
SELECT bureau_history_group, COUNT(*) AS loan_count,
       COUNT(*)::DOUBLE / (SELECT portfolio_loans FROM totals) AS loan_share,
       SUM(loan_default) AS defaults, AVG(loan_default::DOUBLE) AS default_rate
FROM flagged
GROUP BY bureau_history_group;
-- Alternate: use a SUM(CASE...) portfolio share; state the six-month definition explicitly.
