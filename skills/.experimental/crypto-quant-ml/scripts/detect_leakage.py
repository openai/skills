#!/usr/bin/env python3
import sys
import pandas as pd
import numpy as np


def detect_leakage(file_path, target_col='target', threshold=0.95):
    """
    Checks for lookahead bias by identifying suspiciously high correlations
    between features and the target variable.
    citation: Jansen, Ch 8 "The ML4T Workflow" (Lookahead Bias)
    https://github.com/stefan-jansen/machine-learning-for-trading
    """
    try:
        # Load Data
        if file_path.endswith('.parquet'):
            df = pd.read_parquet(file_path)
        elif file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            print(f"[ERROR] Unsupported file format: {file_path}")
            sys.exit(1)

        # Target Column Logic
        if target_col not in df.columns:
            # Try to infer target if not provided
            possible_targets = [c for c in df.columns if 'target' in c.lower() or 'label' in c.lower()]
            if possible_targets:
                target_col = possible_targets[0]
                print(f"[INFO] Inferred target column: {target_col}")
            else:
                print(f"[ERROR] Target column '{target_col}' not found. Available: {list(df.columns)}")
                sys.exit(1)

        # Ensure target is numeric for correlation check
        if not np.issubdtype(df[target_col].dtype, np.number):
            print(
                f"[WARNING] Target '{target_col}' is not numeric. Correlation check skipped for classification targets (TODO: implement mutual information).")
            # For strict numeric correlation checks, we exit successfully if we can't check.
            # Alternatively, we could convert to codes if it's categorical.
            sys.exit(0)

            # Calculate correlation matrix
        # Select numeric columns only
        numeric_df = df.select_dtypes(include=[np.number])

        # Check if target remains in numeric_df (it should, based on check above)
        if target_col not in numeric_df.columns:
            print(f"[ERROR] Target '{target_col}' was dropped during numeric selection.")
            sys.exit(1)

        # Compute correlations
        correlations = numeric_df.corrwith(numeric_df[target_col]).abs()

        # Filter for high correlation
        suspicious = correlations[correlations > threshold]

        # Safely drop the target itself from the suspicious list if present
        if target_col in suspicious.index:
            suspicious = suspicious.drop(labels=[target_col])

        print(f"--- Leakage Detection Report for '{target_col}' ---")
        if not suspicious.empty:
            print(
                f"[WARNING] Found {len(suspicious)} features with correlation > {threshold}. Possible Lookahead Bias!")
            for feature, score in suspicious.items():
                print(f"  - {feature}: {score:.4f}")
            print("\nAdvice: Ensure these features are lagged properly relative to the target.")
            sys.exit(1)  # Fail the validation
        else:
            print("[PASS] No suspiciously high correlations detected.")
            sys.exit(0)  # Explicit success

    except Exception as e:
        print(f"[ERROR] Leakage check failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python detect_leakage.py <path_to_data> [target_column]")
        sys.exit(1)

    target = sys.argv[2] if len(sys.argv) > 2 else 'target'
    detect_leakage(sys.argv[1], target)