# Cleaning Log

**Author:** Kanishk Gupta

Source: generated `docs/DATA_DICTIONARY.md`; labeled training data only for outcome analysis. Raw CSV values are retained as text in staging.

| Field(s) | Choice | Rationale / effect |
|---|---|---|
| `DisbursalDate` | Parse using `%d-%m-%y`; failed parses become NULL. | Source examples use day-month-two-digit-year. |
| `Date.of.Birth` | Parse using `%d-%m-%y`; if parsed DOB is after disbursal, subtract 100 years. | Resolves two-digit-year dates that would otherwise appear in the future. The rule is an assumption; validate against source DOB ranges. |
| `Employment.Type` | Trim, title-case, blank/null -> `Unknown`. | Preserve missingness as an explicit category rather than discard rows. |
| `PERFORM_CNS.SCORE.DESCRIPTION` | Trim; blank/null -> `Unknown`. | Keep source wording; do not infer missing scores from descriptions. |
| `AVERAGE.ACCT.AGE`, `CREDIT.HISTORY.LENGTH` | Parse observed `Xyrs Ymon` string to total months; unparseable -> NULL. | Retain unit as integer months for analysis; all 233,154 training rows parsed for credit history in this supplied file. |
| Numeric source values | `TRY_CAST` to declared numeric/date types; invalid text -> NULL. | Avoid failing the whole build and surface parse issues for future QA. |
| `PERFORM_CNS.SCORE` | Score 0 is retained numerically and categorized as `No score`. | The data dictionary indicates a separate no-history description; numeric zero should not be treated as a valid low score. |
| `Date.of.Birth`, `DisbursalDate` | All 233,154 training rows parsed; derived age range is 18 to 69 years. | No missing parsed dates or implausible (<18 or >100) ages in this supplied file. |
| `ltv` | Retain as source percentage; derive bands `<70`, `70-<80`, `80-<90`, `90%+`. | Bands are transparent analytical buckets, not underwriting cutoffs. |
| `disbursed_amount`, `asset_cost` | Derive ratio `disbursed_amount / asset_cost`; zero/missing asset cost -> NULL. | Safe ratio with denominator check. |
| `loan_default` | Retain 0/1 from train only; test has no label. | Never use the unlabeled test file in rate denominators. |
| Null handling overall | No row-wide deletion or imputation. Keep unknown category for employment and bureau description; numeric nulls remain NULL. | Avoid hidden sample selection and invented values. |

## Validation still recommended

Compare staging and clean row counts; inspect parse failures, future/implausible ages, negative balances, and target values outside 0/1 before treating outputs as decision evidence. Source schema has no branch/state/manufacturer name lookup, so IDs remain codes.
