# Power BI Build Guide

**Author:** Kanishk Gupta

## Load and model

1. Run `python run_all.py`; import the six CSVs in `powerbi/exports/`.
2. Set `date_key` and `disbursal_date` to Date; IDs to whole number; monetary fields to decimal; `loan_default` to whole number.
3. Create one-to-many, single-direction relationships from `dim_date`, `dim_branch`, `dim_state`, `dim_manufacturer`, and `dim_segment` to the fact table.
4. Sort `dim_segment[segment_name]` by `dim_segment[segment_order]`; use the DAX measures in `DAX_MEASURES.md`.
5. The source contains IDs only for branch, state, and manufacturer. Display those IDs as labels unless you obtain an authorized lookup table.

Open `dashboard_preview.html` in a browser for a quick, local view of the same three page themes and current aggregated results. It is a preview, not a Power BI `.pbix` file.

## Page 1 — Portfolio Overview

- KPI cards: loan count, default count, default rate, exposure, exposure at risk.
- Line chart: monthly loan volume and default rate by disbursal month.
- Bar chart: loan volume and default rate by LTV band.
- Slicers: vintage month, state ID, branch ID, manufacturer ID.
- Add a note that the target captures first-EMI default labeling rather than full portfolio performance.

## Page 2 — Risk Drivers

- Matrix: LTV band by bureau score band, values loan count and default rate.
- Bars: default rate by employment type, manufacturer ID, and state ID.
- Scatter or table: branch volume against default rate; filter to branches with at least 250 loans.
- Add data labels/denominators and avoid interpreting descriptive differences as causal.

## Page 3 — Early-Warning Segments

- Stacked column or table: segment loan count, exposure, default count, default rate.
- Trend: vintage-month default rate by risk segment.
- Table: segment, LTV band, bureau score band, recent delinquency, volume, and default rate.
- Include a visible note that segment cutoffs are analyst-selected, require validation, and are not production credit policy.
