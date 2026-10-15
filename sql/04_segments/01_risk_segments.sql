-- EMI Tachometer | Author: Kanishk Gupta
-- PRODUCT DECISION: Kanishk to justify
-- These illustrative, rule-based thresholds are analytical starting points only.
-- Validate stability, fairness, expected capacity, and economics before product use.
-- Priority is Very High, then High, then Medium; otherwise Low.
-- Very High: LTV >= 90% AND (bureau score < 300 / no score OR >= 2 recent delinquencies).
-- High: LTV >= 90% OR (bureau score < 500 / no score AND >= 1 recent delinquency).
-- Medium: LTV >= 80% OR bureau score < 700 OR >= 1 recent delinquency.
-- Missing bureau score is treated as thin/no score, not as a numeric zero risk.
CREATE OR REPLACE VIEW segmented_loans AS
SELECT
    *,
    CASE
        WHEN ltv_pct >= 90
         AND (bureau_score = 0 OR bureau_score < 300 OR delinquent_accounts_6m >= 2)
            THEN 'Very High'
        WHEN ltv_pct >= 90
          OR ((bureau_score = 0 OR bureau_score < 500) AND delinquent_accounts_6m >= 1)
            THEN 'High'
        WHEN ltv_pct >= 80
          OR (bureau_score > 0 AND bureau_score < 700)
          OR delinquent_accounts_6m >= 1
            THEN 'Medium'
        ELSE 'Low'
    END AS risk_segment
FROM fact_loans;

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
