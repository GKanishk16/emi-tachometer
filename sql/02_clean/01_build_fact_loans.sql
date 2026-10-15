-- EMI Tachometer | Author: Kanishk Gupta
-- Convert observed training fields to useful types and derive documented analytics fields.
-- All source columns below are present in docs/DATA_DICTIONARY.md for train.csv.
CREATE OR REPLACE TABLE fact_loans AS
WITH parsed AS (
    SELECT
        TRY_CAST(UniqueID AS BIGINT) AS loan_id,
        TRY_CAST(disbursed_amount AS DECIMAL(18,2)) AS disbursed_amount,
        TRY_CAST(asset_cost AS DECIMAL(18,2)) AS asset_cost,
        TRY_CAST(ltv AS DECIMAL(8,3)) AS ltv_pct,
        TRY_CAST(branch_id AS INTEGER) AS branch_id,
        TRY_CAST(State_ID AS INTEGER) AS state_id,
        TRY_CAST(manufacturer_id AS INTEGER) AS manufacturer_id,
        TRY_CAST(supplier_id AS INTEGER) AS supplier_id,
        -- The source uses DD-MM-YY. TRY_STRPTIME makes bad values NULL for audit.
        TRY_STRPTIME(DisbursalDate, '%d-%m-%y')::DATE AS disbursal_date,
        TRY_STRPTIME("Date.of.Birth", '%d-%m-%y')::DATE AS birth_date_raw,
        NULLIF(TRIM("Employment.Type"), '') AS employment_type_raw,
        TRY_CAST("PERFORM_CNS.SCORE" AS INTEGER) AS bureau_score,
        NULLIF(TRIM("PERFORM_CNS.SCORE.DESCRIPTION"), '') AS bureau_description_raw,
        TRY_CAST("PRI.NO.OF.ACCTS" AS INTEGER) AS primary_accounts,
        TRY_CAST("PRI.OVERDUE.ACCTS" AS INTEGER) AS primary_overdue_accounts,
        TRY_CAST("PRI.CURRENT.BALANCE" AS DECIMAL(18,2)) AS primary_current_balance,
        TRY_CAST("PRI.SANCTIONED.AMOUNT" AS DECIMAL(18,2)) AS primary_sanctioned_amount,
        TRY_CAST("PRI.DISBURSED.AMOUNT" AS DECIMAL(18,2)) AS primary_disbursed_amount,
        TRY_CAST("SEC.NO.OF.ACCTS" AS INTEGER) AS secondary_accounts,
        TRY_CAST("SEC.OVERDUE.ACCTS" AS INTEGER) AS secondary_overdue_accounts,
        TRY_CAST("SEC.CURRENT.BALANCE" AS DECIMAL(18,2)) AS secondary_current_balance,
        TRY_CAST("SEC.SANCTIONED.AMOUNT" AS DECIMAL(18,2)) AS secondary_sanctioned_amount,
        TRY_CAST("SEC.DISBURSED.AMOUNT" AS DECIMAL(18,2)) AS secondary_disbursed_amount,
        TRY_CAST("PRIMARY.INSTAL.AMT" AS DECIMAL(18,2)) AS primary_installment_amount,
        TRY_CAST("SEC.INSTAL.AMT" AS DECIMAL(18,2)) AS secondary_installment_amount,
        TRY_CAST("NEW.ACCTS.IN.LAST.SIX.MONTHS" AS INTEGER) AS new_accounts_6m,
        TRY_CAST("DELINQUENT.ACCTS.IN.LAST.SIX.MONTHS" AS INTEGER) AS delinquent_accounts_6m,
        TRY_CAST("NO.OF_INQUIRIES" AS INTEGER) AS inquiries,
        -- Duration strings are handled in the next CTE; malformed strings remain NULL.
        "AVERAGE.ACCT.AGE" AS average_account_age_raw,
        "CREDIT.HISTORY.LENGTH" AS credit_history_length_raw,
        TRY_CAST(loan_default AS INTEGER) AS loan_default
    FROM staging_train
), normalized AS (
    SELECT
        *,
        -- Source DOBs are two-digit years. If parsing places DOB after disbursal,
        -- interpret it as the previous century; this resolves the observed 20xx ambiguity.
        CASE WHEN birth_date_raw > disbursal_date
             THEN (birth_date_raw - INTERVAL 100 YEAR)::DATE
             ELSE birth_date_raw END AS birth_date,
        CASE WHEN employment_type_raw IS NULL THEN 'Unknown'
             WHEN LOWER(TRIM(employment_type_raw)) = 'salaried' THEN 'Salaried'
             WHEN LOWER(TRIM(employment_type_raw)) = 'self employed' THEN 'Self employed'
             ELSE TRIM(employment_type_raw) END AS employment_type,
        COALESCE(NULLIF(TRIM(bureau_description_raw), ''), 'Unknown') AS bureau_description,
        -- Parse the observed "Xyrs Ymon" format into total months.
        TRY_CAST(REGEXP_EXTRACT(average_account_age_raw, '([0-9]+)yrs? ([0-9]+)mon', 1) AS INTEGER) * 12
          + TRY_CAST(REGEXP_EXTRACT(average_account_age_raw, '([0-9]+)yrs? ([0-9]+)mon', 2) AS INTEGER) AS average_account_age_months,
        TRY_CAST(REGEXP_EXTRACT(credit_history_length_raw, '([0-9]+)yrs? ([0-9]+)mon', 1) AS INTEGER) * 12
          + TRY_CAST(REGEXP_EXTRACT(credit_history_length_raw, '([0-9]+)yrs? ([0-9]+)mon', 2) AS INTEGER) AS credit_history_months
    FROM parsed
), derived AS (
    SELECT
        *,
        DATE_DIFF('year', birth_date, disbursal_date)
          - CASE WHEN STRFTIME(birth_date, '%m-%d') > STRFTIME(disbursal_date, '%m-%d') THEN 1 ELSE 0 END AS age_at_disbursal,
        DATE_TRUNC('month', disbursal_date)::DATE AS vintage_month,
        CASE WHEN ltv_pct IS NULL THEN 'Unknown'
             WHEN ltv_pct < 70 THEN '<70%'
             WHEN ltv_pct < 80 THEN '70-<80%'
             WHEN ltv_pct < 90 THEN '80-<90%'
             ELSE '90%+' END AS ltv_band,
        CASE WHEN bureau_score IS NULL OR bureau_score = 0 THEN 'No score'
             WHEN bureau_score < 300 THEN '<300'
             WHEN bureau_score < 500 THEN '300-499'
             WHEN bureau_score < 700 THEN '500-699'
             ELSE '700+' END AS bureau_score_band,
        CASE WHEN disbursed_amount IS NULL OR asset_cost IS NULL OR asset_cost = 0 THEN NULL
             ELSE disbursed_amount / asset_cost END AS loan_to_asset_ratio
    FROM normalized
)
SELECT
    loan_id,
    CAST(branch_id AS VARCHAR) || '|' || CAST(state_id AS VARCHAR) AS branch_key,
    disbursed_amount, asset_cost, ltv_pct, branch_id, state_id, manufacturer_id,
    supplier_id, disbursal_date, vintage_month, birth_date, age_at_disbursal,
    employment_type, bureau_score, bureau_description, primary_accounts,
    primary_overdue_accounts, primary_current_balance, primary_sanctioned_amount,
    primary_disbursed_amount, secondary_accounts, secondary_overdue_accounts,
    secondary_current_balance, secondary_sanctioned_amount, secondary_disbursed_amount,
    primary_installment_amount, secondary_installment_amount, new_accounts_6m,
    delinquent_accounts_6m, inquiries, average_account_age_months,
    credit_history_months, loan_default, loan_to_asset_ratio, ltv_band,
    bureau_score_band,
    CASE WHEN age_at_disbursal IS NULL THEN 'Unknown'
         WHEN age_at_disbursal < 25 THEN '<25'
         WHEN age_at_disbursal < 35 THEN '25-34'
         WHEN age_at_disbursal < 45 THEN '35-44'
         WHEN age_at_disbursal < 55 THEN '45-54'
         ELSE '55+' END AS age_band
FROM derived;
