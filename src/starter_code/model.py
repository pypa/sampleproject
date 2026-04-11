#!/usr/bin/env python3
"""
model.py — Model definitions and shared constants
==================================================
Central place for all configuration shared across train.py, evaluate.py,
and predict.py.

Exported symbols
----------------
CLINICAL_FEATURES  : list[str]   — clinical covariate column names
CV_FOLDS           : int         — number of stratified CV folds
RANDOM_SEED        : int         — global random seed for reproducibility
MODELS             : dict        — name → sklearn-compatible estimator
build_model(name)  : function    — return a fresh (unfitted) model by name

Sanity check
------------
    python model.py
"""

import os
nslots = int(os.environ.get('NSLOTS', 1))
nslots = nslots - 1 if nslots > 1 else nslots

from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier

# ── Constants ─────────────────────────────────────────────────────────────────

# Clinical features included alongside the 6,592 protein abundances.
CLINICAL_FEATURES = ["age", "sex", "baseline_egfr_23"]

CV_FOLDS    = 5      # stratified k-fold splits for cross-validation
RANDOM_SEED = 42     # controls all random operations for reproducibility

# ── Model definitions ────────────────────────────────────────────────────────
# Each entry: display name → sklearn-compatible estimator.
#
# Design notes:
#   XGBoost  — tree ensemble; scale-invariant; colsample_bytree=0.1 is
#               aggressive feature subsampling that helps with p >> n
#   Lasso LR — linear + L1 penalty; produces sparse solutions (many zero
#               coefficients), making it easy to identify key proteins;
#               StandardScaler is required because LR is scale-sensitive

MODELS = {
    "XGBoost": XGBClassifier(
        n_estimators     = 100,
        max_depth        = 3,        # shallow trees reduce overfitting
        learning_rate    = 0.1,
        subsample        = 0.8,
        colsample_bytree = 0.1,      # sample 10 % of features per tree
        eval_metric      = "logloss",
        random_state     = RANDOM_SEED,
        n_jobs           = nslots,
    ),
    "Lasso LR": Pipeline([
        ("scaler", StandardScaler()),
        ("clf", LogisticRegression(
            penalty      = "l1",
            solver       = "liblinear",
            C            = 0.1,      # strong regularisation for p >> n
            max_iter     = 1000,
            random_state = RANDOM_SEED,
        )),
    ]),
}


# ── Factory function ──────────────────────────────────────────────────────────

def build_model(name: str):
    """
    Return a fresh (unfitted) model by name.

    >>> from model import build_model
    >>> clf = build_model("XGBoost")
    >>> clf.fit(X_train, y_train)
    """
    from sklearn.base import clone
    if name not in MODELS:
        raise ValueError(f"Unknown model '{name}'. Choose from: {list(MODELS)}")
    return clone(MODELS[name])


if __name__ == "__main__":
    import numpy as np

    print("Models defined:")
    for name in MODELS:
        m = build_model(name)
        print(f"  {name}: {type(m).__name__}")

    print(f"\nClinical features : {CLINICAL_FEATURES}")
    print(f"CV folds          : {CV_FOLDS}")
    print(f"Random seed       : {RANDOM_SEED}")

    # Quick smoke test
    rng = np.random.default_rng(0)
    X_dummy = rng.standard_normal((50, 10))
    y_dummy = rng.integers(0, 2, 50)
    for name in MODELS:
        m = build_model(name)
        m.fit(X_dummy, y_dummy)
        proba = m.predict_proba(X_dummy)
        assert proba.shape == (50, 2), "predict_proba shape mismatch"
        print(f"  [{name}] smoke test passed")
