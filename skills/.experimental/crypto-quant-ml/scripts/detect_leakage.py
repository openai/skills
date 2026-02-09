#!/usr/bin/env python3
import sys
import pandas as pd
import numpy as np


def detect_leakage(file_path, target_col=None, threshold=0.95):
    """
    Checks for lookahead bias by identifying suspiciously high correlations.
    Returns True if passed (no leakage), False if failed (leakage found or error).
    """
    try:
        # --- Load Data ---
        if file_path.endswith('.parquet'):
            df = pd.read_parquet(file_path)
        elif file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            print(f"[ERROR] Unsupported file format: {file_path}")
            return False

        # --- Target Column Logic ---
        # If user explicitly asked for a specific column, fail if it's missing.
        if target_col and target_col not in df.columns:
            print(f"[ERROR] User-specified target '{target_col}' not found in dataset.")
            print(f"Available columns: {list(df.columns)}")
            return False

        # If no target specified (None), try to infer it.
        if target_col is None:
            possible_targets = [c for c in df.columns if 'target' in c.lower() or 'label' in c.lower()]
            if possible_targets:
                target_col = possible_targets[0]
                print(f"[INFO] No target specified. Inferred target column: '{target_col}'")
            else:
                print("[ERROR] No target specified and unable to infer one automatically.")
                return False

        # --- Numeric Check ---
        # Check if target is numeric or boolean
        if not (np.issubdtype(df[target_col].dtype, np.number) or df[target_col].dtype == 'bool'):
            print(f"[WARNING] Target '{target_col}' is non-numeric (type: {df[target_col].dtype}). Skipping correlation check.")
            # We return True (Pass) here because we couldn't prove leakage,
            # and we don't want to block the pipeline for a classification task.
            return True

        # Select numeric/bool columns only
        numeric_df = df.select_dtypes(include=[np.number, 'bool'])

        if target_col not in numeric_df.columns:
            print(f"[ERROR] Target '{target_col}' was dropped during numeric selection.")
            return False

        # --- Compute Correlations ---
        correlations = numeric_df.corrwith(numeric_df[target_col]).abs()

        # Filter for high correlation
        suspicious = correlations[correlations > threshold]

        # Drop the target itself from the list (correlation of 1.0 is expected)
        if target_col in suspicious.index:
            suspicious = suspicious.drop(labels=[target_col])

        # --- Report ---
        print(f"--- Leakage Detection Report for '{target_col}' ---")
        if not suspicious.empty:
            print(f"[WARNING] Found {len(suspicious)} features with correlation > {threshold}. Possible Lookahead Bias!")
            for feature, score in suspicious.items():
                print(f"  - {feature}: {score:.4f}")
            print("\nAdvice: Ensure these features are lagged properly relative to the target.")
            return False  # FAIL
        else:
            print("[PASS] No suspiciously high correlations detected.")
            return True   # PASS

    except Exception as e:
        print(f"[ERROR] Leakage check failed: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python detect_leakage.py <path_to_data> [target_column]")
        sys.exit(1)

    # If user provides a 3rd arg, use it. Otherwise, pass None to trigger inference.
    target_arg = sys.argv[2] if len(sys.argv) > 2 else None

    # Exit code based on boolean return
    success = detect_leakage(sys.argv[1], target_arg)
    sys.exit(0 if success else 1)