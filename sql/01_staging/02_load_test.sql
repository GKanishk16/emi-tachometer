-- EMI Tachometer | Author: Kanishk Gupta
-- Load the unlabeled competition test CSV separately; it is not used in default rates.
-- Run from the repository root after placing test_bqCt9Pv.csv in data/raw/.
CREATE OR REPLACE TABLE staging_test AS
SELECT *
FROM read_csv('data/raw/test_bqCt9Pv.csv', header = true, all_varchar = true);
