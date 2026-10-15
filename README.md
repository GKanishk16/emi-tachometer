# EMI Tachometer

**Author:** Kanishk Gupta  
**Status:** Schema discovery first. Add the manually downloaded CSV files to `data/raw/`; the profile is required before building schema-dependent transformations and analyses.

## Business problem

This project will turn vehicle-loan application and outcome data into portfolio views, explainable rule-based risk segments, and product recommendations for a lending-software company. It is designed as an SQL-first portfolio analytics project, not a production credit decision system.

## Dataset

Source: [L&T Vehicle Loan Default Prediction on Kaggle](https://www.kaggle.com/datasets/mamtadhaker/lt-vehicle-loan-default-prediction). Download and place the CSV files in `data/raw/` yourself. This repository does not download or redistribute the data. Review and follow the dataset's Kaggle license and attribution terms before use or publication. If the license terms do not permit your intended use, do not publish the data or derived material that the terms restrict.

## Current first step

The project deliberately profiles the actual files before making schema assumptions:

```bash
python -m pip install -r requirements.txt
python src/profile_data.py
```

This writes `docs/DATA_DICTIONARY.md` with observed column names, pandas dtypes, null percentages, distinct counts, sample values, and cautious interpretations marked **Inferred**. Verify interpretations against the source documentation. Schema-dependent SQL, cleaning choices, export dimensions, and findings must be based on that generated dictionary.

## Planned architecture

- Python 3.11+ orchestrates local runs; pandas handles CSV profiling and Power BI exports.
- DuckDB stores the project in a single ignored `.duckdb` file.
- Readable, commented standalone DuckDB SQL owns staging, cleaning, analysis, and rule-based segment logic.
- Power BI consumes star-schema CSV exports and documented DAX measures.

## Limitations to document in the finished analysis

The dataset is historical and may not reflect current lending conditions. An application/default label does not provide a repayment time series, delinquency progression, recoveries, or realized loss. Associations in the data are descriptive and do not establish causality. Segment rules will need product, risk, and compliance review before operational use.

## License

The project code is released under the MIT License in `LICENSE`. The dataset remains subject to its separate Kaggle license.
