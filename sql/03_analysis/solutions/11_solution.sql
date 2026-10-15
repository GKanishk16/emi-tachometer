-- EMI Tachometer | Author: Kanishk Gupta
-- Q11: Test a descriptive high-risk segment formed from three observable attributes.
WITH tagged AS (
    SELECT *,
       CASE WHEN ltv_pct >= 90
              AND (bureau_score = 0 OR bureau_score < 500)
              AND delinquent_accounts_6m >= 1
            THEN 'Candidate high risk' ELSE 'Other loans' END AS candidate_segment
    FROM fact_loans
)
SELECT candidate_segment, COUNT(*) AS loan_count,
       SUM(disbursed_amount) AS exposure, SUM(loan_default) AS defaults,
       AVG(loan_default::DOUBLE) AS default_rate
FROM tagged
GROUP BY candidate_segment;
-- Alternate: express the rules in a reusable view/table so multiple queries share one definition.
