# Rule-Based Segment Cutoff Rationale

**Author:** Kanishk Gupta

The SQL file `sql/04_segments/01_risk_segments.sql` keeps all operational cutoffs together in its `product_cutoffs` CTE. The following rationale explains why these values are legible starting points and what the supplied data does—and does not—justify.

| Cutoff | Rationale for this exploratory version | Evidence and limitation |
|---|---|---|
| LTV 80% and 90% | Reuse the LTV bands in the analysis so that segment and driver results are comparable. | The 80–<90% group is 25.88% default vs 16.15% for <70%; 90%+ is 22.64% with only 1,219 loans. The upper band does not continue the monotonic pattern. |
| Bureau score 300, 500, 700 | Align the rules with the score bands exposed in the portfolio analysis; distinguish very low, low, and below-700 scores. | The 300–499 band is 29.32%, while 700+ is 15.79%; `<300` is 21.53% and no-score is 23.13%. The score relationship is not monotonic, so score alone should not determine a segment. |
| No-score value 0 | Keep the observed source convention for unavailable bureau history separate from a valid numeric score. | The raw data has 116,950 rows with score 0 / no bureau history description; it is a meaningful information-availability flag, not an imputed score. |
| One recent delinquent account | Treat any reported delinquent account in the prior-six-month count as a review signal for High/Medium rules. | This is an interpretable trigger, but the source gives a count of accounts, not dates, severity, cures, or borrower-level payment performance. |
| Two recent delinquent accounts | Reserve Very High for repeated/multiple-account delinquency when combined with very high LTV. | This raises rule specificity, but is not calibrated to expected loss or an intervention capacity target. |

## Observed segment result

| Segment | Loans | Default rate |
|---|---:|---:|
| Low | 110,937 | 18.75% |
| Medium | 113,869 | 24.01% |
| High | 7,948 | 29.59% |
| Very High | 400 | 30.50% |

The ordered rates are directionally useful for a triage prototype, but High and Very High are close, and the Very High group is small. The cutoffs are therefore **explainable analyst hypotheses**, not optimized thresholds or a claim of calibrated probability. Validate with newer vintages, repayment outcomes, fairness review, and prospective testing before using them in live decisions.
