# EMI Tachometer

**Author:** Kanishk Gupta  
**Status:** Complete against the supplied CSVs. Re-run the profile and pipeline after changing raw inputs.

## Business problem

This project will turn vehicle-loan application and outcome data into portfolio views, explainable rule-based risk segments, and product recommendations for a lending-software company. It is designed as an SQL-first portfolio analytics project, not a production credit decision system.

## Dataset

Source: [L&T Vehicle Loan Default Prediction on Kaggle](https://www.kaggle.com/datasets/mamtadhaker/lt-vehicle-loan-default-prediction). Download and place the CSV files in `data/raw/` yourself. This repository does not download or redistribute the data. Review and follow the dataset's Kaggle license and attribution terms before use or publication. If the license terms do not permit your intended use, do not publish the data or derived material that the terms restrict.

## Run end to end

Place the manually downloaded `train.csv` and `test_bqCt9Pv.csv` in `data/raw/`, then run one command from the repository root:

```bash
python -m pip install -r requirements.txt
python run_all.py
```

The run refreshes `docs/DATA_DICTIONARY.md`, builds a local `emi_tachometer.duckdb`, regenerates the Power BI star-schema extracts in `powerbi/exports/`, and refreshes a browser-viewable 3-page dashboard preview at `powerbi/dashboard_preview.html`. To refresh the schema profile independently, run `python src/profile_data.py`.

The project deliberately profiles the actual files before making schema assumptions:

```bash
python src/profile_data.py
```

This writes `docs/DATA_DICTIONARY.md` with observed column names, pandas dtypes, null percentages, distinct counts, sample values, and cautious interpretations marked **Inferred**. Verify interpretations against the source documentation. The SQL and cleaning choices in this repository were built from the supplied profile.

## Architecture

- Python 3.11+ orchestrates local runs; pandas handles CSV profiling and Power BI exports.
- DuckDB stores the project in a single ignored `.duckdb` file.
- Readable, commented standalone DuckDB SQL owns staging, cleaning, analysis, and rule-based segment logic.
- Power BI consumes star-schema CSV exports and documented DAX measures; a lightweight HTML preview provides a runnable visual without claiming to be a `.pbix` file.

## Tests and optional baseline

Run the SQL integration checks with `python -m unittest discover -s tests`. They execute every solution and executable pipeline SQL file against the supplied data and verify the question files remain comment-only. The optional logistic baseline is secondary; its current random holdout ROC AUC is recorded in `docs/MODEL_BASELINE.md`.

## Limitations

The dataset is historical and may not reflect current lending conditions. An application/default label does not provide a repayment time series, delinquency progression, recoveries, or realized loss. Associations in the data are descriptive and do not establish causality. Segment rules will need product, risk, and compliance review before operational use.

## License

The project code is released under the MIT License in `LICENSE`. The dataset remains subject to its separate Kaggle license.
