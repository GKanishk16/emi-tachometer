-- EMI Tachometer | Author: Kanishk Gupta
-- Q6: Inspect whether LTV and bureau score interact in observed default rates.
SELECT ltv_band,                                  -- collateral leverage category
       bureau_score_band,                         -- credit score category
       COUNT(*) AS loan_count,                    -- cell size
       SUM(loan_default) AS defaults,             -- event count
       AVG(loan_default::DOUBLE) AS default_rate  -- cell default share
FROM fact_loans
GROUP BY ltv_band, bureau_score_band               -- cross classification
ORDER BY ltv_band, bureau_score_band;
-- Alternate: use conditional aggregation to pivot score bands into columns.
