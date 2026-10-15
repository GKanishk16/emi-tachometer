-- EMI Tachometer | Author: Kanishk Gupta
-- Q8: Rank branches from lowest to highest observed default rate.
WITH branch_metrics AS (
    SELECT branch_id, COUNT(*) AS loan_count, SUM(loan_default) AS defaults,
           AVG(loan_default::DOUBLE) AS default_rate
    FROM fact_loans
    GROUP BY branch_id
    HAVING COUNT(*) >= 250                         -- suppress very small groups
)
SELECT branch_id, loan_count, defaults, default_rate,
       RANK() OVER (ORDER BY default_rate ASC) AS branch_rank -- ties share rank
FROM branch_metrics
ORDER BY branch_rank, branch_id;
-- Alternate: DENSE_RANK removes gaps after ties; ROW_NUMBER forces unique ranks.
