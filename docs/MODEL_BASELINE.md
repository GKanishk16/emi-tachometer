# Optional Logistic Regression Baseline

**Author:** Kanishk Gupta

A random stratified 75/25 holdout split produced a ROC AUC of **0.6273** with the current feature set and a balanced logistic regression. Reproduce with `python src/model_baseline.py` after `python run_all.py`.

This is a secondary sanity check, not the project objective or an underwriting model. The random split does not test forward-in-time generalization; branch/state and historical application variables may encode dataset-specific effects; AUC does not establish calibration, fairness, causal effects, or business value. The target is the dataset's first-EMI default label and there is no repayment timeline or realized-loss target. Feature effects should be interpreted only as model associations.
