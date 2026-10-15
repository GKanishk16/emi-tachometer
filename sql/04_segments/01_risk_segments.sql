-- EMI Tachometer | Author: Kanishk Gupta
-- PRODUCT DECISION: Kanishk to justify
-- Illustrative rule-based thresholds only; validate stability, fairness, capacity,
-- and economics before any product use. Priority is Very High, High, Medium, then Low.
-- Missing bureau score is treated as thin/no score rather than a valid low score.
CREATE OR REPLACE VIEW segmented_loans AS
WITH product_cutoffs AS (
    -- The only location for numeric cutoffs used by operational segment rules.
    SELECT 90::DECIMAL AS very_high_ltv_pct,
           80::DECIMAL AS medium_ltv_pct,
           300::INTEGER AS very_low_bureau_score,
           500::INTEGER AS low_bureau_score,
           700::INTEGER AS medium_bureau_score,
           0::INTEGER AS no_score_value,
           2::INTEGER AS very_high_delinquency_min,
           1::INTEGER AS delinquency_min
)
SELECT
    loans.*,
    CASE
        WHEN loans.ltv_pct >= cutoffs.very_high_ltv_pct
         AND (loans.bureau_score = cutoffs.no_score_value
              OR loans.bureau_score < cutoffs.very_low_bureau_score
              OR loans.delinquent_accounts_6m >= cutoffs.very_high_delinquency_min)
            THEN 'Very High'
        WHEN loans.ltv_pct >= cutoffs.very_high_ltv_pct
          OR ((loans.bureau_score = cutoffs.no_score_value
               OR loans.bureau_score < cutoffs.low_bureau_score)
              AND loans.delinquent_accounts_6m >= cutoffs.delinquency_min)
            THEN 'High'
        WHEN loans.ltv_pct >= cutoffs.medium_ltv_pct
          OR (loans.bureau_score > cutoffs.no_score_value
              AND loans.bureau_score < cutoffs.medium_bureau_score)
          OR loans.delinquent_accounts_6m >= cutoffs.delinquency_min
            THEN 'Medium'
        ELSE 'Low'
    END AS risk_segment
FROM fact_loans AS loans
CROSS JOIN product_cutoffs AS cutoffs;

-- Final output: segment volume, funded exposure and observed default rate.
SELECT
    risk_segment,
    COUNT(*) AS loan_count,
    SUM(disbursed_amount) AS exposure,
    SUM(CASE WHEN loan_default = 1 THEN disbursed_amount ELSE 0 END) AS defaulted_exposure,
    SUM(loan_default) AS defaults,
    AVG(loan_default::DOUBLE) AS default_rate
FROM segmented_loans
GROUP BY risk_segment
ORDER BY CASE risk_segment WHEN 'Very High' THEN 1 WHEN 'High' THEN 2 WHEN 'Medium' THEN 3 ELSE 4 END;
