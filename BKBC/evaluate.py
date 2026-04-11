#!/usr/bin/env python3
"""
evaluate.py — Cross-validation for model development
======================================================
Runs stratified k-fold cross-validation on the BKBC training data to
estimate model performance. Use this to iterate on your model before
final submission.

Both XGBoost and Lasso LR are evaluated with the same CV protocol so
their performance is directly comparable.

USAGE
-----
    python evaluate.py
    python evaluate.py --data /path/to/BKBC_train/train.csv
    python evaluate.py --data /path/to/train.csv --folds 10

OUTPUTS  (written to --out directory)
-------
    cv_confusion_matrix_{model}.png  — k-fold CV confusion matrix per model
    cv_results.csv                   — per-fold metrics for all models
"""

import argparse
import logging
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
    roc_auc_score,
    log_loss,
)

from model import MODELS, CV_FOLDS, RANDOM_SEED, build_model
from preprocess import load_data, build_features_and_labels

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(message)s",
    datefmt="%H:%M:%S",
)

_SCRIPT_DIR   = Path(__file__).resolve().parent
_DEFAULT_DATA = _SCRIPT_DIR.parent.parent / "BKBC_train" / "train.csv"
_DEFAULT_OUT  = _SCRIPT_DIR.parent.parent / "results"


def parse_args():
    p = argparse.ArgumentParser(
        description="Run cross-validation on BKBC training data."
    )
    p.add_argument(
        "--data",
        default=str(_DEFAULT_DATA),
        help="Path to training CSV (default: ../../BKBC_train/train.csv)",
    )
    p.add_argument(
        "--out",
        default=str(_DEFAULT_OUT),
        help="Directory for CV outputs (default: ../../results/)",
    )
    p.add_argument(
        "--folds",
        type=int,
        default=CV_FOLDS,
        help=f"Number of CV folds (default: {CV_FOLDS})",
    )
    return p.parse_args()


def run_cv(model, X, y, n_folds, name):
    """Run stratified k-fold CV and return out-of-fold predictions."""
    cv = StratifiedKFold(n_splits=n_folds, shuffle=True, random_state=RANDOM_SEED)
    logging.info(f"[{name}] Running {n_folds}-fold CV...")

    y_prob = cross_val_predict(model, X, y, cv=cv, method="predict_proba")[:, 1]
    y_pred = (y_prob >= 0.5).astype(int)

    # Per-fold metrics
    fold_results = []
    for fold_idx, (train_idx, val_idx) in enumerate(cv.split(X, y)):
        y_val = y[val_idx]
        p_val = y_prob[val_idx]
        fold_auc = roc_auc_score(y_val, p_val) if len(np.unique(y_val)) > 1 else float("nan")
        fold_ll  = log_loss(y_val, p_val)
        fold_results.append({
            "model": name,
            "fold": fold_idx,
            "n_samples": len(val_idx),
            "n_ati": y_val.sum(),
            "auc": fold_auc,
            "log_loss": fold_ll,
        })

    return y_pred, y_prob, fold_results


def print_metrics(y, y_pred, y_prob, title):
    """Print classification metrics."""
    print(f"\n=== {title} ===")
    print(classification_report(y, y_pred, target_names=["No ATI", "ATI"]))
    if len(np.unique(y)) > 1:
        print(f"AUC (ROC):  {roc_auc_score(y, y_prob):.3f}")
    print(f"Log loss:   {log_loss(y, y_prob):.3f}")


def plot_confusion_matrix(y, y_pred, out_path, title, n_folds):
    """Save a confusion matrix plot."""
    fig, ax = plt.subplots(figsize=(5, 4))
    ConfusionMatrixDisplay(
        confusion_matrix(y, y_pred),
        display_labels=["No ATI", "ATI"],
    ).plot(ax=ax, colorbar=False)
    ax.set_title(f"ATI — {n_folds}-Fold CV — {title}")
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    logging.info(f"Saved: {out_path}")
    plt.close()


def main():
    args    = parse_args()
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    df = load_data(args.data)
    X, y, feature_cols = build_features_and_labels(df)

    all_fold_results = []

    for name in MODELS:
        print("\n" + "=" * 60)
        print(f"MODEL: {name}")
        print("=" * 60)

        model = build_model(name)
        y_pred, y_prob, fold_results = run_cv(model, X, y, args.folds, name)
        all_fold_results.extend(fold_results)

        print_metrics(y, y_pred, y_prob, f"{name} — {args.folds}-Fold CV")

        slug = name.lower().replace(" ", "_")
        plot_confusion_matrix(
            y, y_pred,
            out_dir / f"cv_confusion_matrix_{slug}.png",
            title=name,
            n_folds=args.folds,
        )

    # Save per-fold results
    results_df = pd.DataFrame(all_fold_results)
    results_df.to_csv(out_dir / "cv_results.csv", index=False)
    logging.info(f"Saved: {out_dir / 'cv_results.csv'}")

    # Summary table
    print("\n" + "=" * 60)
    print(f"{'Model':<12} | {'Mean AUC':>10} | {'Std AUC':>10} | {'Mean LogLoss':>13}")
    print("-" * 60)
    for name in MODELS:
        m = results_df[results_df["model"] == name]
        print(f"{name:<12} | {m['auc'].mean():>10.3f} | {m['auc'].std():>10.3f} | {m['log_loss'].mean():>13.3f}")
    print("=" * 60)

    print(f"\nAll outputs saved to {out_dir}/")


if __name__ == "__main__":
    main()
