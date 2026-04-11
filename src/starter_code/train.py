#!/usr/bin/env python3
"""
train.py — Train a model on BKBC data and save weights
========================================================
Loads the combat-corrected BKBC training CSV, trains an XGBoost classifier
on ALL samples (no train/test split), and saves the model weights.

The saved model is used by predict.py / predict.sh for inference.

USAGE
-----
    python train.py --data /path/to/BKBC_train/train.csv  # Training on any other data will result in disqualification

OUTPUTS  (written to weights/ directory)
-------
    weights/xgboost_model.json   — trained XGBoost model
    weights/feature_cols.json    — ordered feature column list
"""

import argparse
import json
import logging
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score, log_loss

from model import RANDOM_SEED, build_model
from preprocess import load_data, build_features_and_labels

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(message)s",
    datefmt="%H:%M:%S",
)

_SCRIPT_DIR     = Path(__file__).resolve().parent
_DEFAULT_DATA   = _SCRIPT_DIR.parent.parent / "BKBC_train" / "train.csv"
_DEFAULT_WEIGHTS = _SCRIPT_DIR / "weights"


def parse_args():
    p = argparse.ArgumentParser(
        description="Train XGBoost on BKBC data and save model weights."
    )
    p.add_argument(
        "--data",
        default=str(_DEFAULT_DATA),
        help="Path to training CSV (default: ../../BKBC_train/train.csv)",
    )
    p.add_argument(
        "--out",
        default=str(_DEFAULT_WEIGHTS),
        help="Directory to save model weights (default: ./weights/)",
    )
    p.add_argument(
        "--model-name",
        default="XGBoost",
        help="Model to train (default: XGBoost)",
    )
    return p.parse_args()


def main():
    args    = parse_args()
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Load data
    df = load_data(args.data)
    X, y, feature_cols = build_features_and_labels(df)

    # Train on all data
    model = build_model(args.model_name)
    logging.info(f"Training {args.model_name} on {len(y)} samples...")
    model.fit(X, y)

    # Training set metrics (for sanity check only)
    y_prob = model.predict_proba(X)[:, 1]
    auc = roc_auc_score(y, y_prob)
    ll  = log_loss(y, y_prob)

    print(f"\n{'=' * 50}")
    print(f"  Model     : {args.model_name}")
    print(f"  Samples   : {len(y)} (ATI={y.sum()}, No ATI={(y==0).sum()})")
    print(f"  Features  : {len(feature_cols)}")
    print(f"  Train AUC : {auc:.3f}")
    print(f"  Train Loss: {ll:.3f}")
    print(f"{'=' * 50}")

    # Save model
    model_path = out_dir / "xgboost_model.json"
    model.save_model(str(model_path))
    logging.info(f"Saved model: {model_path}")

    # Save feature columns
    features_path = out_dir / "feature_cols.json"
    with open(features_path, "w") as f:
        json.dump(feature_cols, f)
    logging.info(f"Saved features: {features_path}")

    # Feature importance summary
    if hasattr(model, "feature_importances_"):
        importance = pd.DataFrame({
            "feature": feature_cols,
            "gain": model.feature_importances_,
        }).sort_values("gain", ascending=False)

        csv_path = out_dir / "feature_importance.csv"
        importance.to_csv(csv_path, index=False)
        logging.info(f"Saved feature importance: {csv_path}")

        print("\nTop 10 features by XGBoost gain:")
        print(importance.head(10).to_string(index=False))

    print(f"\nWeights saved to {out_dir}/")
    print("Next step: bash predict.sh /path/to/new_data.csv")


if __name__ == "__main__":
    main()
