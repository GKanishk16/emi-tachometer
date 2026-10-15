# Power BI DAX Measures

**Author:** Kanishk Gupta

Load `fact_loans.csv` and dimensions from `powerbi/exports/`. Create one-to-many relationships from each dimension's key to `fact_loans` (`dim_date[date_key]` to `fact_loans[disbursal_date]`; branch, state, manufacturer IDs; segment name). Mark `dim_date` as the date table. It is exported as a continuous daily calendar across the observed period so time-intelligence measures work.

```DAX
Loan Count = COUNTROWS(fact_loans)

Defaults = SUM(fact_loans[loan_default])

Default Rate = DIVIDE([Defaults], [Loan Count])

Exposure = SUM(fact_loans[disbursed_amount])

Exposure at Risk =
CALCULATE([Exposure], fact_loans[loan_default] = 1)

Portfolio Default Rate =
CALCULATE([Default Rate], REMOVEFILTERS(dim_segment), REMOVEFILTERS(fact_loans[segment_name]))

Default Rate vs Portfolio Average = [Default Rate] - [Portfolio Default Rate]

Segment Share =
DIVIDE([Loan Count], CALCULATE([Loan Count], REMOVEFILTERS(dim_segment), REMOVEFILTERS(fact_loans[segment_name])))

Prior Month Default Rate =
CALCULATE([Default Rate], DATEADD(dim_date[date_key], -1, MONTH))

MoM Default Rate Change = [Default Rate] - [Prior Month Default Rate]
```

`Exposure at Risk` means original disbursed principal for loans labeled default in the dataset; it is not outstanding balance, expected loss, or loss given default. MoM compares historical origination cohorts and their dataset labels; this dataset has no dated repayment trajectory.
