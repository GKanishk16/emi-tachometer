"""Export a simple star-schema CSV package with pandas. Author: Kanishk Gupta."""
from pathlib import Path
import pandas as pd
import duckdb


def export_all(connection: duckdb.DuckDBPyConnection, output_dir: Path) -> None:
    """Write fact and dimensions using pandas so users can inspect/edit exports."""
    output_dir.mkdir(parents=True, exist_ok=True)
    queries = {
        'fact_loans': """SELECT loan_id, disbursal_date, vintage_month, branch_key, branch_id, state_id,
            manufacturer_id, risk_segment AS segment_name, disbursed_amount, asset_cost,
            ltv_pct, loan_to_asset_ratio, ltv_band, bureau_score, bureau_score_band,
            employment_type, age_at_disbursal, age_band, credit_history_months,
            delinquent_accounts_6m, loan_default
            FROM segmented_loans""",
        'dim_branch': "SELECT DISTINCT CAST(branch_id AS VARCHAR) || '|' || CAST(state_id AS VARCHAR) AS branch_key, branch_id, state_id FROM fact_loans ORDER BY branch_id, state_id",
        'dim_state': "SELECT DISTINCT state_id FROM fact_loans ORDER BY state_id",
        'dim_manufacturer': "SELECT DISTINCT manufacturer_id FROM fact_loans ORDER BY manufacturer_id",
        'dim_date': """WITH bounds AS (SELECT MIN(disbursal_date) AS first_date, MAX(disbursal_date) AS last_date FROM fact_loans)
            SELECT CAST(calendar.day AS DATE) AS date_key,
            EXTRACT(YEAR FROM calendar.day)::INTEGER AS year,
            EXTRACT(QUARTER FROM calendar.day)::INTEGER AS quarter,
            EXTRACT(MONTH FROM calendar.day)::INTEGER AS month_number,
            STRFTIME(calendar.day, '%B') AS month_name,
            DATE_TRUNC('month', calendar.day)::DATE AS vintage_month
            FROM bounds, generate_series(bounds.first_date, bounds.last_date, INTERVAL 1 DAY) AS calendar(day)
            ORDER BY date_key""",
        'dim_segment': """SELECT * FROM (VALUES
            ('Low', 1), ('Medium', 2), ('High', 3), ('Very High', 4)
            ) AS segments(segment_name, segment_order)""",
    }
    for table, query in queries.items():
        frame = connection.execute(query).fetchdf()
        frame.to_csv(output_dir / f'{table}.csv', index=False)
        print(f'Exported {table}: {len(frame):,} rows')
