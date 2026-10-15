-- EMI Tachometer | Author: Kanishk Gupta
-- Q10: Build a concentration curve from observable risk indicators, not the target.
WITH ordered AS (
    SELECT loan_id, loan_default,
       ROW_NUMBER() OVER (ORDER BY delinquent_accounts_6m DESC,
                          bureau_score ASC, ltv_pct DESC, loan_id) AS risk_rank,
       COUNT(*) OVER () AS portfolio_loans,
       SUM(loan_default) OVER () AS portfolio_defaults
    FROM fact_loans
), cumulative AS (
    SELECT *,
       SUM(loan_default) OVER (ORDER BY risk_rank ROWS UNBOUNDED PRECEDING) AS defaults_to_rank
    FROM ordered
)
SELECT CEIL(risk_rank / 10000.0) AS risk_rank_bucket,
       MAX(risk_rank) AS loans_in_bucket,
       MAX(risk_rank)::DOUBLE / MAX(portfolio_loans) AS cumulative_loan_share,
       MAX(defaults_to_rank)::DOUBLE / NULLIF(MAX(portfolio_defaults), 0) AS cumulative_default_share
FROM cumulative
GROUP BY risk_rank_bucket
ORDER BY risk_rank_bucket;
-- Alternate: use NTILE(100) for percentiles, aggregating ties/unequal bucket sizes as needed.
