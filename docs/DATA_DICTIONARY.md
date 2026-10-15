# Data Dictionary

Author: Kanishk Gupta

> Generated from the CSV files currently present in `data/raw/`. Interpretations are heuristic and explicitly **inferred**; validate them against the source documentation. Re-run `python src/profile_data.py` after changing the raw files.

## `data/raw/test_bqCt9Pv.csv`

Rows: 112,392 · Columns: 40

| Column | pandas dtype | Null % | Unique count | Sample values | Interpretation |
|---|---|---:|---:|---|---|
| UniqueID | int64 | 0.00% | 112,392 | 655269, 723482, 758529, 763449, 708663 | Inferred: may be an identifier or code. Validate with the dataset documentation before use. |
| disbursed_amount | int64 | 0.00% | 14,525 | 53478, 55513, 65282, 46905, 51428 | Inferred: may represent a loan or repayment measure. Validate with the dataset documentation before use. |
| asset_cost | int64 | 0.00% | 29,383 | 63558, 63163, 84320, 63896, 71211 | Inferred: may describe the financed vehicle. Validate with the dataset documentation before use. |
| ltv | float64 | 0.00% | 5,902 | 86.54, 89.45, 79.93, 76.58, 86.08 | Inferred: observed as float64; meaning is not established from the profile alone. Validate with the dataset documentation before use. |
| branch_id | int64 | 0.00% | 82 | 67, 78, 34, 130, 74 | Inferred: may represent geography or servicing location; may be an identifier or code. Validate with the dataset documentation before use. |
| supplier_id | int64 | 0.00% | 2,863 | 22807, 23135, 17014, 17502, 15196 | Inferred: may be an identifier or code. Validate with the dataset documentation before use. |
| manufacturer_id | int64 | 0.00% | 11 | 45, 86, 51, 48, 49 | Inferred: may describe the financed vehicle; may be an identifier or code. Validate with the dataset documentation before use. |
| Current_pincode_ID | int64 | 0.00% | 6,202 | 1497, 2071, 2070, 2069, 2103 | Inferred: may represent geography or servicing location; may be an identifier or code. Validate with the dataset documentation before use. |
| Date.of.Birth | str | 0.00% | 14,052 | 01-01-74, 20-05-85, 14-10-95, 01-06-73, 01-06-72 | Inferred: may represent a date or time attribute; may represent borrower or asset age. Validate with the dataset documentation before use. |
| Employment.Type | str | 3.06% | 2 | Salaried, Self employed | Inferred: may describe borrower employment or income. Validate with the dataset documentation before use. |
| DisbursalDate | str | 0.00% | 27 | 03-11-18, 20-11-18, 29-11-18, 17-11-18, 21-11-18 | Inferred: may represent a date or time attribute; may represent a loan or repayment measure. Validate with the dataset documentation before use. |
| State_ID | int64 | 0.00% | 22 | 6, 4, 3, 5, 10 | Inferred: may represent geography or servicing location; may be an identifier or code. Validate with the dataset documentation before use. |
| Employee_code_ID | int64 | 0.00% | 3,143 | 1998, 1646, 1863, 1570, 1835 | Inferred: may be an identifier or code. Validate with the dataset documentation before use. |
| MobileNo_Avl_Flag | int64 | 0.00% | 1 | 1 | Inferred: observed as int64; meaning is not established from the profile alone. Validate with the dataset documentation before use. |
| Aadhar_flag | int64 | 0.00% | 2 | 1, 0 | Inferred: observed as int64; meaning is not established from the profile alone. Validate with the dataset documentation before use. |
| PAN_flag | int64 | 0.00% | 2 | 0, 1 | Inferred: observed as int64; meaning is not established from the profile alone. Validate with the dataset documentation before use. |
| VoterID_flag | int64 | 0.00% | 2 | 0, 1 | Inferred: may be an identifier or code. Validate with the dataset documentation before use. |
| Driving_flag | int64 | 0.00% | 2 | 0, 1 | Inferred: observed as int64; meaning is not established from the profile alone. Validate with the dataset documentation before use. |
| Passport_flag | int64 | 0.00% | 2 | 0, 1 | Inferred: observed as int64; meaning is not established from the profile alone. Validate with the dataset documentation before use. |
| PERFORM_CNS.SCORE | int64 | 0.00% | 566 | 0, 749, 14, 383, 783 | Inferred: may represent credit bureau information. Validate with the dataset documentation before use. |
| PERFORM_CNS.SCORE.DESCRIPTION | str | 0.00% | 19 | No Bureau History Available, C-Very Low Risk, Not Scored: Only a Guarantor, K-High Risk, B-Very Low Risk | Inferred: may represent credit bureau information. Validate with the dataset documentation before use. |
| PRI.NO.OF.ACCTS | int64 | 0.00% | 83 | 0, 2, 1, 5, 7 | Inferred: observed as int64; meaning is not established from the profile alone. Validate with the dataset documentation before use. |
| PRI.ACTIVE.ACCTS | int64 | 0.00% | 32 | 0, 1, 4, 3, 2 | Inferred: observed as int64; meaning is not established from the profile alone. Validate with the dataset documentation before use. |
| PRI.OVERDUE.ACCTS | int64 | 0.00% | 16 | 0, 1, 2, 3, 7 | Inferred: observed as int64; meaning is not established from the profile alone. Validate with the dataset documentation before use. |
| PRI.CURRENT.BALANCE | int64 | 0.00% | 35,550 | 0, 43898, 132480, 336355, 583108 | Inferred: observed as int64; meaning is not established from the profile alone. Validate with the dataset documentation before use. |
| PRI.SANCTIONED.AMOUNT | int64 | 0.00% | 21,721 | 0, 48780, 255000, 333290, 600000 | Inferred: may represent a loan or repayment measure. Validate with the dataset documentation before use. |
| PRI.DISBURSED.AMOUNT | int64 | 0.00% | 23,343 | 0, 48780, 255000, 333290, 600000 | Inferred: may represent a loan or repayment measure. Validate with the dataset documentation before use. |
| SEC.NO.OF.ACCTS | int64 | 0.00% | 23 | 0, 1, 5, 9, 2 | Inferred: observed as int64; meaning is not established from the profile alone. Validate with the dataset documentation before use. |
| SEC.ACTIVE.ACCTS | int64 | 0.00% | 15 | 0, 2, 1, 6, 8 | Inferred: observed as int64; meaning is not established from the profile alone. Validate with the dataset documentation before use. |
| SEC.OVERDUE.ACCTS | int64 | 0.00% | 7 | 0, 1, 2, 3, 7 | Inferred: observed as int64; meaning is not established from the profile alone. Validate with the dataset documentation before use. |
| SEC.CURRENT.BALANCE | int64 | 0.00% | 742 | 0, 6231, 2288998, 299536, 257959 | Inferred: observed as int64; meaning is not established from the profile alone. Validate with the dataset documentation before use. |
| SEC.SANCTIONED.AMOUNT | int64 | 0.00% | 610 | 0, 43500, 39000, 2494000, 387000 | Inferred: may represent a loan or repayment measure. Validate with the dataset documentation before use. |
| SEC.DISBURSED.AMOUNT | int64 | 0.00% | 663 | 0, 43500, 39000, 2230081, 387000 | Inferred: may represent a loan or repayment measure. Validate with the dataset documentation before use. |
| PRIMARY.INSTAL.AMT | int64 | 0.00% | 17,125 | 0, 5605, 2122, 8398, 25165 | Inferred: observed as int64; meaning is not established from the profile alone. Validate with the dataset documentation before use. |
| SEC.INSTAL.AMT | int64 | 0.00% | 470 | 0, 8159, 21328, 2762, 3643 | Inferred: observed as int64; meaning is not established from the profile alone. Validate with the dataset documentation before use. |
| NEW.ACCTS.IN.LAST.SIX.MONTHS | int64 | 0.00% | 20 | 0, 1, 2, 3, 4 | Inferred: may represent a date or time attribute. Validate with the dataset documentation before use. |
| DELINQUENT.ACCTS.IN.LAST.SIX.MONTHS | int64 | 0.00% | 13 | 0, 1, 2, 4, 8 | Inferred: may represent a date or time attribute. Validate with the dataset documentation before use. |
| AVERAGE.ACCT.AGE | str | 0.00% | 176 | 0yrs 0mon, 0yrs 8mon, 2yrs 5mon, 1yrs 7mon, 1yrs 11mon | Inferred: may represent borrower or asset age; sample values suggest a duration field. Validate with the dataset documentation before use. |
| CREDIT.HISTORY.LENGTH | str | 0.00% | 252 | 0yrs 0mon, 1yrs 0mon, 2yrs 5mon, 2yrs 2mon, 2yrs 6mon | Inferred: may represent credit bureau information; sample values suggest a duration field. Validate with the dataset documentation before use. |
| NO.OF_INQUIRIES | int64 | 0.00% | 22 | 0, 1, 3, 2, 5 | Inferred: observed as int64; meaning is not established from the profile alone. Validate with the dataset documentation before use. |

## `data/raw/train.csv`

Rows: 233,154 · Columns: 41

| Column | pandas dtype | Null % | Unique count | Sample values | Interpretation |
|---|---|---:|---:|---|---|
| UniqueID | int64 | 0.00% | 233,154 | 420825, 537409, 417566, 624493, 539055 | Inferred: may be an identifier or code. Validate with the dataset documentation before use. |
| disbursed_amount | int64 | 0.00% | 24,565 | 50578, 47145, 53278, 57513, 52378 | Inferred: may represent a loan or repayment measure. Validate with the dataset documentation before use. |
| asset_cost | int64 | 0.00% | 46,252 | 58400, 65550, 61360, 66113, 60300 | Inferred: may describe the financed vehicle. Validate with the dataset documentation before use. |
| ltv | float64 | 0.00% | 6,579 | 89.55, 73.23, 89.63, 88.48, 88.39 | Inferred: observed as float64; meaning is not established from the profile alone. Validate with the dataset documentation before use. |
| branch_id | int64 | 0.00% | 82 | 67, 78, 34, 130, 74 | Inferred: may represent geography or servicing location; may be an identifier or code. Validate with the dataset documentation before use. |
| supplier_id | int64 | 0.00% | 2,953 | 22807, 22744, 17014, 20700, 15196 | Inferred: may be an identifier or code. Validate with the dataset documentation before use. |
| manufacturer_id | int64 | 0.00% | 11 | 45, 86, 48, 51, 120 | Inferred: may describe the financed vehicle; may be an identifier or code. Validate with the dataset documentation before use. |
| Current_pincode_ID | int64 | 0.00% | 6,698 | 1441, 1502, 1497, 1501, 1495 | Inferred: may represent geography or servicing location; may be an identifier or code. Validate with the dataset documentation before use. |
| Date.of.Birth | str | 0.00% | 15,433 | 01-01-84, 31-07-85, 24-08-85, 30-12-93, 09-12-77 | Inferred: may represent a date or time attribute; may represent borrower or asset age. Validate with the dataset documentation before use. |
| Employment.Type | str | 3.29% | 2 | Salaried, Self employed | Inferred: may describe borrower employment or income. Validate with the dataset documentation before use. |
| DisbursalDate | str | 0.00% | 84 | 03-08-18, 26-09-18, 01-08-18, 26-10-18, 19-09-18 | Inferred: may represent a date or time attribute; may represent a loan or repayment measure. Validate with the dataset documentation before use. |
| State_ID | int64 | 0.00% | 22 | 6, 4, 3, 9, 5 | Inferred: may represent geography or servicing location; may be an identifier or code. Validate with the dataset documentation before use. |
| Employee_code_ID | int64 | 0.00% | 3,270 | 1998, 1646, 115, 1863, 1570 | Inferred: may be an identifier or code. Validate with the dataset documentation before use. |
| MobileNo_Avl_Flag | int64 | 0.00% | 1 | 1 | Inferred: observed as int64; meaning is not established from the profile alone. Validate with the dataset documentation before use. |
| Aadhar_flag | int64 | 0.00% | 2 | 1, 0 | Inferred: observed as int64; meaning is not established from the profile alone. Validate with the dataset documentation before use. |
| PAN_flag | int64 | 0.00% | 2 | 0, 1 | Inferred: observed as int64; meaning is not established from the profile alone. Validate with the dataset documentation before use. |
| VoterID_flag | int64 | 0.00% | 2 | 0, 1 | Inferred: may be an identifier or code. Validate with the dataset documentation before use. |
| Driving_flag | int64 | 0.00% | 2 | 0, 1 | Inferred: observed as int64; meaning is not established from the profile alone. Validate with the dataset documentation before use. |
| Passport_flag | int64 | 0.00% | 2 | 0, 1 | Inferred: observed as int64; meaning is not established from the profile alone. Validate with the dataset documentation before use. |
| PERFORM_CNS.SCORE | int64 | 0.00% | 573 | 0, 598, 305, 825, 17 | Inferred: may represent credit bureau information. Validate with the dataset documentation before use. |
| PERFORM_CNS.SCORE.DESCRIPTION | str | 0.00% | 20 | No Bureau History Available, I-Medium Risk, L-Very High Risk, A-Very Low Risk, Not Scored: Not Enough Info available on the customer | Inferred: may represent credit bureau information. Validate with the dataset documentation before use. |
| PRI.NO.OF.ACCTS | int64 | 0.00% | 108 | 0, 1, 3, 2, 7 | Inferred: observed as int64; meaning is not established from the profile alone. Validate with the dataset documentation before use. |
| PRI.ACTIVE.ACCTS | int64 | 0.00% | 40 | 0, 1, 2, 5, 4 | Inferred: observed as int64; meaning is not established from the profile alone. Validate with the dataset documentation before use. |
| PRI.OVERDUE.ACCTS | int64 | 0.00% | 22 | 0, 1, 3, 2, 14 | Inferred: observed as int64; meaning is not established from the profile alone. Validate with the dataset documentation before use. |
| PRI.CURRENT.BALANCE | int64 | 0.00% | 71,341 | 0, 27600, 72879, -41, 676 | Inferred: observed as int64; meaning is not established from the profile alone. Validate with the dataset documentation before use. |
| PRI.SANCTIONED.AMOUNT | int64 | 0.00% | 44,390 | 0, 50200, 74500, 365384, 36154 | Inferred: may represent a loan or repayment measure. Validate with the dataset documentation before use. |
| PRI.DISBURSED.AMOUNT | int64 | 0.00% | 47,909 | 0, 50200, 74500, 365384, 23374 | Inferred: may represent a loan or repayment measure. Validate with the dataset documentation before use. |
| SEC.NO.OF.ACCTS | int64 | 0.00% | 37 | 0, 2, 1, 3, 11 | Inferred: observed as int64; meaning is not established from the profile alone. Validate with the dataset documentation before use. |
| SEC.ACTIVE.ACCTS | int64 | 0.00% | 23 | 0, 2, 1, 3, 11 | Inferred: observed as int64; meaning is not established from the profile alone. Validate with the dataset documentation before use. |
| SEC.OVERDUE.ACCTS | int64 | 0.00% | 9 | 0, 1, 4, 5, 3 | Inferred: observed as int64; meaning is not established from the profile alone. Validate with the dataset documentation before use. |
| SEC.CURRENT.BALANCE | int64 | 0.00% | 3,246 | 0, 1171994, 5787530, 29870, 4683 | Inferred: observed as int64; meaning is not established from the profile alone. Validate with the dataset documentation before use. |
| SEC.SANCTIONED.AMOUNT | int64 | 0.00% | 2,223 | 0, 1690000, 40000, 6425000, 34458 | Inferred: may represent a loan or repayment measure. Validate with the dataset documentation before use. |
| SEC.DISBURSED.AMOUNT | int64 | 0.00% | 2,553 | 0, 1690000, 361, 6425000, 34458 | Inferred: may represent a loan or repayment measure. Validate with the dataset documentation before use. |
| PRIMARY.INSTAL.AMT | int64 | 0.00% | 28,067 | 0, 1991, 31, 1347, 2608 | Inferred: observed as int64; meaning is not established from the profile alone. Validate with the dataset documentation before use. |
| SEC.INSTAL.AMT | int64 | 0.00% | 1,918 | 0, 9382, 6485, 1563, 1065 | Inferred: observed as int64; meaning is not established from the profile alone. Validate with the dataset documentation before use. |
| NEW.ACCTS.IN.LAST.SIX.MONTHS | int64 | 0.00% | 26 | 0, 1, 4, 2, 6 | Inferred: may represent a date or time attribute. Validate with the dataset documentation before use. |
| DELINQUENT.ACCTS.IN.LAST.SIX.MONTHS | int64 | 0.00% | 14 | 0, 1, 2, 3, 5 | Inferred: may represent a date or time attribute. Validate with the dataset documentation before use. |
| AVERAGE.ACCT.AGE | str | 0.00% | 192 | 0yrs 0mon, 1yrs 11mon, 0yrs 8mon, 1yrs 9mon, 0yrs 2mon | Inferred: may represent borrower or asset age; sample values suggest a duration field. Validate with the dataset documentation before use. |
| CREDIT.HISTORY.LENGTH | str | 0.00% | 294 | 0yrs 0mon, 1yrs 11mon, 1yrs 3mon, 2yrs 0mon, 0yrs 2mon | Inferred: may represent credit bureau information; sample values suggest a duration field. Validate with the dataset documentation before use. |
| NO.OF_INQUIRIES | int64 | 0.00% | 25 | 0, 1, 4, 2, 3 | Inferred: observed as int64; meaning is not established from the profile alone. Validate with the dataset documentation before use. |
| loan_default | int64 | 0.00% | 2 | 0, 1 | Inferred: may represent a target or outcome; may represent a loan or repayment measure. Validate with the dataset documentation before use. |
