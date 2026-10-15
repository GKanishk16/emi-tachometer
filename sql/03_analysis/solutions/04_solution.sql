-- EMI Tachometer | Author: Kanishk Gupta
-- Q4: Show the ten highest and lowest qualifying state/branch rates.
WITH grouped AS (
    SELECT 'State' AS geography_type, state_id AS geography_id,
           COUNT(*) AS loan_count, SUM(loan_default) AS defaults,
           AVG(loan_default::DOUBLE) AS default_rate
    FROM fact_loans GROUP BY state_id
    UNION ALL
    SELECT 'Branch', branch_id, COUNT(*), SUM(loan_default), AVG(loan_default::DOUBLE)
    FROM fact_loans GROUP BY branch_id
), eligible AS (
    SELECT * FROM grouped WHERE loan_count >= 250 -- minimum-volume guardrail
), ranked AS (
    SELECT *, RANK() OVER (PARTITION BY geography_type ORDER BY default_rate DESC) AS high_rank,
              RANK() OVER (PARTITION BY geography_type ORDER BY default_rate ASC) AS low_rank
    FROM eligible
)
SELECT geography_type, geography_id, loan_count, defaults, default_rate, 'Highest' AS extreme, high_rank AS rate_rank
FROM ranked WHERE high_rank <= 10
UNION ALL
SELECT geography_type, geography_id, loan_count, defaults, default_rate, 'Lowest' AS extreme, low_rank AS rate_rank
FROM ranked WHERE low_rank <= 10
ORDER BY geography_type, extreme, rate_rank;
-- Alternate: use ROW_NUMBER for exactly ten entries; RANK preserves ties.
