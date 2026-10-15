-- EMI Tachometer | Author: Kanishk Gupta
-- Q3: Compare outcomes by observed employment category.
SELECT
    employment_type,                            -- standardized value or Unknown
    COUNT(*) AS loan_count,                     -- denominator
    SUM(loan_default) AS defaults,              -- observed defaults
    AVG(loan_default::DOUBLE) AS default_rate   -- default share
FROM fact_loans
GROUP BY employment_type                        -- preserve missingness category
ORDER BY default_rate DESC;                     -- rank from highest rate
-- Alternate: calculate rates with SUM(default)/NULLIF(COUNT(*),0).
