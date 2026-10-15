-- EMI Tachometer | Author: Kanishk Gupta
-- Load the labeled Kaggle training CSV as text so raw values remain auditable.
-- Run from the repository root after placing train.csv in data/raw/.
CREATE OR REPLACE TABLE staging_train AS
SELECT *
FROM read_csv('data/raw/train.csv', header = true, all_varchar = true);
