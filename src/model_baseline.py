"""Optional logistic sanity check. Analytics remain the project's primary purpose.
Author: Kanishk Gupta
"""
from pathlib import Path
import duckdb
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    connection = duckdb.connect(str(ROOT / 'emi_tachometer.duckdb'), read_only=True)
    try:
        frame = connection.execute('SELECT * FROM fact_loans').fetchdf()
    finally:
        connection.close()
    numeric = ['disbursed_amount', 'asset_cost', 'ltv_pct', 'branch_id', 'state_id',
               'manufacturer_id', 'age_at_disbursal', 'bureau_score',
               'primary_overdue_accounts', 'primary_accounts', 'credit_history_months',
               'delinquent_accounts_6m', 'inquiries']
    categorical = ['employment_type', 'ltv_band', 'bureau_score_band']
    x_train, x_test, y_train, y_test = train_test_split(
        frame[numeric + categorical], frame['loan_default'], test_size=0.25,
        random_state=42, stratify=frame['loan_default'])
    prep = ColumnTransformer([
        ('numeric', Pipeline([('impute', SimpleImputer(strategy='median')),
                              ('scale', StandardScaler())]), numeric),
        ('categorical', Pipeline([('impute', SimpleImputer(strategy='most_frequent')),
                                  ('encode', OneHotEncoder(handle_unknown='ignore'))]), categorical),
    ])
    model = Pipeline([('prepare', prep), ('logistic', LogisticRegression(max_iter=1000, class_weight='balanced'))])
    model.fit(x_train, y_train)
    auc = roc_auc_score(y_test, model.predict_proba(x_test)[:, 1])
    print(f'Holdout ROC AUC (25% random stratified split): {auc:.4f}')
    print('Sanity check only: random split, historical first-EMI label, possible temporal/geographic leakage; not a production model.')


if __name__ == '__main__':
    main()
