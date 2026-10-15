-- EMI Tachometer | Author: Kanishk Gupta
-- Q7: Show origination cohort default rates by disbursal month.
SELECT vintage_month,                             -- month derived from disbursal date
       COUNT(*) AS loan_count,                     -- cohort size
       SUM(loan_default) AS defaults,              -- target positives
       AVG(loan_default::DOUBLE) AS default_rate   -- cohort rate
FROM fact_loans
GROUP BY vintage_month
ORDER BY vintage_month;
-- Alternate: derive DATE_TRUNC('month', disbursal_date) at query time.
