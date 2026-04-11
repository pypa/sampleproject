#!/bin/bash
# predict.sh — Predict ATI probability for samples in a CSV
# ===========================================================
# Usage:
#     bash predict.sh <input.csv> [output.csv]
#
# Arguments:
#     input.csv   — CSV with the same feature columns as the training data
#     output.csv  — (optional) path for predictions (default: predictions.csv)
#
# Example:
#     bash predict.sh ../../BKBC_train/train.csv
#     bash predict.sh /path/to/new_samples.csv my_predictions.csv

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ $# -lt 1 ]; then
    echo "Usage: bash predict.sh <input.csv> [output.csv]"
    echo ""
    echo "Predict ATI probability for each sample in the input CSV."
    exit 1
fi

# Activate virtual environment
source "$SCRIPT_DIR/.venv/bin/activate" # Participants, please hardcode the path to YOUR TEAM's desired virtual env. This is the venv we will activate for evaluation.

INPUT="$1"
OUTPUT="${2:-predictions.csv}"

python3 "$SCRIPT_DIR/predict.py" \
    --data "$INPUT" \
    --out  "$OUTPUT"
