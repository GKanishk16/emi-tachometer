-- EMI Tachometer | Author: Kanishk Gupta
-- Q2: Compare default rate across numeric bureau-score bands.
SELECT
    bureau_score_band,                         -- report the cleaned score band
    COUNT(*) AS loan_count,                    -- include denominator for context
    SUM(loan_default) AS defaults,             -- count observed target positives
    AVG(loan_default::DOUBLE) AS default_rate  -- binary mean is the rate
FROM fact_loans
GROUP BY bureau_score_band                     -- one row per score band
ORDER BY CASE bureau_score_band                -- order bands numerically
    WHEN 'No score' THEN 1 WHEN '<300' THEN 2 WHEN '300-499' THEN 3
    WHEN '500-699' THEN 4 ELSE 5 END;
-- Alternate: group by source bureau description for more granular categories.
