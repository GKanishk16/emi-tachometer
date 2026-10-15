"""Integration checks that every executable DuckDB SQL file runs. Author: Kanishk Gupta."""
from pathlib import Path
import unittest
import duckdb

ROOT = Path(__file__).resolve().parents[1]


class SQLIntegrationTests(unittest.TestCase):
    def test_all_sql_files_run_or_are_question_only(self) -> None:
        connection = duckdb.connect(':memory:')
        try:
            execution_order = [
                'sql/01_staging/01_load_train.sql',
                'sql/01_staging/02_load_test.sql',
                'sql/02_clean/01_build_fact_loans.sql',
                'sql/04_segments/01_risk_segments.sql',
            ]
            executed = set()
            for relative in execution_order:
                connection.execute((ROOT / relative).read_text())
                executed.add(relative)
            for path in sorted((ROOT / 'sql').rglob('*.sql')):
                relative = path.relative_to(ROOT).as_posix()
                if relative.startswith('sql/03_analysis/questions/'):
                    question_text = path.read_text().strip()
                    self.assertTrue(question_text.startswith('/*') and question_text.endswith('*/'))
                    continue
                if relative not in executed:
                    connection.execute(path.read_text())
            self.assertEqual(connection.execute('SELECT COUNT(*) FROM fact_loans').fetchone()[0], 233154)
            self.assertEqual(connection.execute('SELECT COUNT(*) FROM staging_test').fetchone()[0], 112392)
            self.assertEqual(connection.execute('SELECT COUNT(*) FROM fact_loans WHERE loan_default NOT IN (0,1)').fetchone()[0], 0)
            self.assertGreater(connection.execute('SELECT COUNT(*) FROM fact_loans WHERE credit_history_months IS NOT NULL').fetchone()[0], 200000)
            self.assertEqual(connection.execute("SELECT COUNT(*) - COUNT(DISTINCT branch_key) FROM (SELECT DISTINCT CAST(branch_id AS VARCHAR) || '|' || CAST(state_id AS VARCHAR) AS branch_key FROM fact_loans)").fetchone()[0], 0)
        finally:
            connection.close()


if __name__ == '__main__':
    unittest.main()
