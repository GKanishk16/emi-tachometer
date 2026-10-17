#!/usr/bin/env python3
"""Build the local DuckDB model and Power BI CSV package. Author: Kanishk Gupta."""
from pathlib import Path
import duckdb
from src.export_powerbi import export_all
from src.profile_data import write_dictionary
from src.build_dashboard_preview import build as build_dashboard_preview

ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / 'emi_tachometer.duckdb'


def run_sql(connection: duckdb.DuckDBPyConnection, relative_path: str) -> None:
    sql = (ROOT / relative_path).read_text(encoding='utf-8')
    connection.execute(sql)
    print(f'Executed {relative_path}')


def main() -> None:
    missing = [name for name in ('train.csv', 'test_bqCt9Pv.csv') if not (ROOT / 'data/raw' / name).exists()]
    if missing:
        raise SystemExit(f'Missing required raw file(s) in data/raw/: {", ".join(missing)}')
    # Refresh the data dictionary before building any schema-dependent tables.
    raw_files = sorted((ROOT / 'data/raw').glob('*.csv'))
    write_dictionary(raw_files, sample_size=5)
    connection = duckdb.connect(str(DB_PATH))
    try:
        for sql_path in ('sql/01_staging/01_load_train.sql', 'sql/01_staging/02_load_test.sql',
                         'sql/02_clean/01_build_fact_loans.sql', 'sql/04_segments/01_risk_segments.sql'):
            run_sql(connection, sql_path)
        export_all(connection, ROOT / 'powerbi' / 'exports')
        build_dashboard_preview(connection)
    finally:
        connection.close()
    print(f'Build complete: {DB_PATH}')


if __name__ == '__main__':
    main()
