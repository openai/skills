#!/usr/bin/env python3
import sys
import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller


def validate_stationarity(file_path, target_col='close', significance_level=0.05):
    """
    Validates stationarity using ADF.
    Returns True if stationary (raw or diff), False otherwise.
    """
    try:
        # --- Data Loading ---
        if file_path.endswith('.parquet'):
            df = pd.read_parquet(file_path)
        elif file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            print(f"[ERROR] Unsupported file format: {file_path}")
            return False

        if target_col not in df.columns:
            print(f"[ERROR] Column '{target_col}' not found. Available: {list(df.columns)}")
            return False

        # --- Statistical Pre-processing ---
        # Business Time logic: dropna() stitches gaps, preserving volatility.
        series = df[target_col].dropna()

        if len(series) < 20:
            print("[ERROR] Not enough data points to test stationarity.")
            return False

        if not np.issubdtype(series.dtype, np.number):
            print(f"[ERROR] Column '{target_col}' is not numeric.")
            return False

        if series.nunique() <= 1:
            print("[FAIL] Series is constant. Cannot test stationarity.")
            return False

        # --- Run ADF on Raw Series ---
        print(f"--- Running ADF Test on raw '{target_col}' ---")

        # Tuple unpacking prevents IDE warnings about return types
        adf_stat, p_value, *_ = adfuller(series)

        print(f"ADF Statistic: {adf_stat:.4f}")
        print(f"p-value: {p_value:.4f}")

        if p_value < significance_level:
            print("[PASS] Raw series is stationary.")
            return True

        # --- Run ADF on Differenced Series ---
        print("[FAIL] Raw series is Non-Stationary. Attempting differencing...")
        print(f"--- Running ADF Test on Returns of '{target_col}' ---")

        # Handle non-positive values for log returns
        if (series <= 0).any():
            print("[WARNING] Series contains <= 0 values. Using simple pct_change.")
            returns = series.pct_change()
        else:
            # Context manager for clean logs, handle Inf/NaNs
            with np.errstate(divide='ignore', invalid='ignore'):
                returns = np.log(series / series.shift(1))

        # Boolean indexing handles both Series and Arrays safely
        returns = returns[np.isfinite(returns)]

        if returns.empty:
            print("[ERROR] Differencing resulted in empty series.")
            return False

        adf_stat_diff, p_value_diff, *_ = adfuller(returns)

        print(f"ADF Statistic (Diff): {adf_stat_diff:.4f}")
        print(f"p-value (Diff): {p_value_diff:.4f}")

        if p_value_diff < significance_level:
            print("[PASS] Differenced series is stationary.")
            return True
        else:
            print("[CRITICAL] Even differenced series is non-stationary.")
            return False

    except Exception as e:
        print(f"[ERROR] Stationarity check failed: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_stationarity.py <path_to_data> [target_column]")
        sys.exit(1)

    target = sys.argv[2] if len(sys.argv) > 2 else 'close'

    # Exit code based on boolean return
    success = validate_stationarity(sys.argv[1], target)
    sys.exit(0 if success else 1)