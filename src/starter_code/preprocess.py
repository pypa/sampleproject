#!/usr/bin/env python3
"""
preprocess.py — Data loading helpers
=====================================
Loads the pre-processed, combat-corrected CSV files and extracts the
feature matrix and binary ATI labels.

Used by train.py, evaluate.py, and predict.py.

LABELS
------
Binary ATI (derived from biopsy histopathology):
    0 = No ATI
    1 = ATI present

FEATURES
--------
    Proteomics : 6,592 log2-normalised, combat-corrected SomaScan abundances
                 (anonymised as feature_XXXX columns)
    Clinical   : age, sex, baseline_egfr_23

USAGE
-----
    from preprocess import load_data, build_features_and_labels
    df = load_data("/path/to/train.csv")
    X, y, feature_cols = build_features_and_labels(df)
"""

import logging
from pathlib import Path

import numpy as np
import pandas as pd

from model import CLINICAL_FEATURES

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(message)s",
    datefmt="%H:%M:%S",
)


def load_data(data_path: str) -> pd.DataFrame:
    """
    Load a pre-processed CSV (train.csv or test CSV).

    The CSV is expected to have columns:
        sample_id, ati, age, sex, baseline_egfr_23, feature_XXXX...
    """
    logging.info(f"Loading data from {data_path}...")
    df = pd.read_csv(data_path, low_memory=False, na_values=[".", ""])
    logging.info(f"  {len(df)} samples, {len(df.columns)} columns")
    return df


def build_features_and_labels(df: pd.DataFrame):
    """
    Extract the feature matrix X and binary ATI label vector y.

    Feature set = anonymised protein columns (feature_XXXX) + CLINICAL_FEATURES.
    Rows missing any feature or the ATI label are dropped (complete-case analysis).

    Returns
    -------
    X            : np.ndarray  (n_samples, n_features)
    y            : np.ndarray  (n_samples,)  0 = No ATI, 1 = ATI
    feature_cols : list[str]   column names in the same order as X columns
    """
    protein_cols = sorted([c for c in df.columns if c.startswith("feature_")])
    feature_cols = protein_cols + CLINICAL_FEATURES

    # Check which features are available
    available = [c for c in feature_cols if c in df.columns]
    missing = [c for c in feature_cols if c not in df.columns]
    if missing:
        logging.warning(f"{len(missing)} feature columns missing from data")
    feature_cols = available

    required = feature_cols + ["ati"]
    df_clean = df[required].copy().dropna(subset=required)

    n_dropped = len(df) - len(df_clean)
    if n_dropped:
        logging.warning(f"Dropped {n_dropped} rows with missing values")

    y = df_clean["ati"].astype(int).values
    X = df_clean[feature_cols].values

    logging.info(
        f"Samples: {len(df_clean)} | No ATI: {(y == 0).sum()} | ATI: {(y == 1).sum()}"
    )
    logging.info(
        f"Features: {sum(c.startswith('feature_') for c in feature_cols)} protein"
        f" + {sum(not c.startswith('feature_') for c in feature_cols)} clinical"
        f" = {len(feature_cols)} total"
    )
    return X, y, feature_cols
