# EMI Tachometer — Portfolio Findings and Product Recommendations

**Author:** Kanishk Gupta  
**Analysis date:** 2026-10-17  
**Dataset:** L&T Vehicle Loan Default Prediction, labeled training file. Monetary figures below remain in the dataset's reported units; no currency metadata was assumed.

## Portfolio snapshot

- Labeled loans: **233,154**
- Defaults: **50,611**
- Overall labeled default rate: **21.71%**
- Total disbursed principal: **12,673,550,469**
- Disbursed principal on default-labeled loans: **2,847,904,953** (not outstanding balance or realized loss)
- Disbursal dates: **2018-08-01 to 2018-10-31**

## Three findings

### 1. Bureau score bands differ, but the pattern is not monotonic

The 300–499 band has a **29.32%** default rate (17,154 loans), compared with **15.79%** for 700+ (51,825 loans). The `<300` band is **21.53%** and the no-score group is **23.13%**, so the data does not support a simple “lower score always means higher default” rule.

**SQL proof:** `sql/03_analysis/solutions/02_solution.sql`  
**Caveat:** First-EMI default labels are historical, and score bands may reflect sample composition or source-specific scoring. Treat this as descriptive.

### 2. The 80–<90% LTV band has the highest rate among LTV bands

The 80–<90% LTV band has a **25.88%** rate (81,159 loans); the `<70%` band is **16.15%** (65,365 loans). The 90%+ band is **22.64%** but includes only **1,219 loans**, and therefore does not establish a monotonic increase at the upper end.

**SQL proof:** `sql/03_analysis/solutions/01_solution.sql`  
**Caveat:** The supplied LTV is a source field; the highest LTV group is small. Avoid treating these associations as a causal cap recommendation.

### 3. Bureau score and LTV together expose a concentrated higher-rate cell

Within the 80–<90% LTV band, loans with bureau scores 300–499 have a **33.09%** rate (6,941 loans), versus **25.15%** for scores 500–699 (13,548 loans). The joint cut gives more context than either attribute alone.

**SQL proof:** `sql/03_analysis/solutions/06_solution.sql`  
**Caveat:** This is a retrospective cell comparison, not evidence that changing LTV or score policy will cause a change in defaults. Check the rates in new cohorts before productizing.

## Product recommendations for a lending platform

### 1. Add a configurable early-collections prioritization trigger

**Product behavior:** Allow lenders to route High and Very High rule-based segments into a prioritized pre-due-date welcome/contact queue, with an explanation of the flags and a human override. Avoid automatic adverse action.

**Evidence:** The High and Very High segments contain **8,348 loans (3.58% of the portfolio)** and **2,474 defaults (4.89% of all labeled defaults)**. Their historical default rates are 29.59% and 30.50%, respectively, versus 21.71% overall.

**Expected impact:** The historical data suggests a small, higher-rate cohort can be prioritized for service. It cannot estimate preventable defaults or collection savings. Measure contact completion, first-payment delinquency, complaints, and incremental outcomes against a comparable control group in a prospective pilot.

**Risks:** The dataset has no repayment timeline, contact history, treatment response, or cost-to-serve data. A first-EMI default label is not a collections strategy test. Review fairness, consent, contact rules, and operational capacity.

### 2. Add a multi-signal application review / policy simulator

**Product behavior:** Let a lender configure a second-look queue for combinations such as LTV 80–<90% and bureau score 300–499. Show the contributing attributes, configurable thresholds, historical volumes, and outcome rates; preserve an override and audit trail. Do not apply a blanket LTV cap from this dataset alone.

**Evidence:** That joint cell has 6,941 loans and a 33.09% labeled default rate. The broader LTV results are nonmonotonic, and the 90%+ group is small, so the feature should help lenders compare and monitor policy scenarios rather than assert a single optimal cutoff.

**Expected impact:** Make risk review more targeted and policy changes measurable. Quantify any approval, default, or loss impact only through prospective evaluation with repayment outcomes and appropriate comparison groups.

**Risks:** Historical selection bias, adverse impact, stale bureau data, low-volume cells, and feedback loops can distort apparent performance. Keep the final policy with the lender and audit outcome rates by relevant groups.

## Data needed next

- Dated repayment schedules and payment events, including days past due, cures, recoveries, and write-offs.
- Application-time bureau snapshots with timestamps and reason codes.
- Approved and declined applications, loan terms, pricing, and collateral valuations.
- Collections contacts, treatment assignment, outcomes, costs, and consent/compliance flags.
- Authoritative branch, state, and manufacturer lookup tables.
- Multiple newer origination vintages to validate temporal stability and policy impact.

## Interpretation limits

This dataset covers a short 2018 disbursal window and a first-EMI default label. It does not include a full repayment time series, outstanding balances, realized loss, interventions, or causal identification. Rates and segments here are an analytical portfolio exercise, not validated credit policy.
