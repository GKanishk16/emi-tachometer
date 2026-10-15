-- EMI Tachometer | Author: Kanishk Gupta
-- Q5: Compare outcomes by the available manufacturer code.
SELECT manufacturer_id,                        -- source provides ID only
       COUNT(*) AS loan_count,                  -- volume denominator
       SUM(loan_default) AS defaults,           -- default count
       AVG(loan_default::DOUBLE) AS default_rate
FROM fact_loans
GROUP BY manufacturer_id
ORDER BY default_rate DESC, loan_count DESC;
-- Alternate: join an authoritative manufacturer lookup if one becomes available.
