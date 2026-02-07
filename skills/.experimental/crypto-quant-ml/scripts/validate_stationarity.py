#!/usr/bin/env python3
import sys
import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller


def validate_stationarity(file_path, target_col='close', significance_level=0.05):
    """
    Validates stationarity of a time series using the Augmented Dickey-Fuller test.
    citation: Jansen, Ch 9 "Time-Series Models" & Lopez de Prado, Ch 5 "Fractionally Differentiated Features"
    https://github.com/stefan-jansen/machine-learning-for-trading
    https://www.wiley.com/en-us/Advances+in+Financial+Machine+Learning-p-9781119482086
    """
    try:
        # Load Data
        if file_path.endswith('.parquet'):
            df = pd.read_parquet(file_path)
        elif file_path.endswith('.csv'):
            df = pd.read_csv(file_path, parse_dates=True, index_col=0)
        else:
            print(f"[ERROR] Unsupported file format: {file_path}")
            sys.exit(1)

        # Validate Column Exists
        if target_col not in df.columns:
            print(f"[ERROR] Column '{target_col}' not found in dataset. Available: {list(df.columns)}")
            sys.exit(1)

        # Pre-process: Drop NaNs and Ensure Numeric
        series = df[target_col].dropna()
        if not np.issubdtype(series.dtype, np.number):
            print(f"[ERROR] Column '{target_col}' is not numeric.")
            sys.exit(1)

        # Run ADF on raw series
        print(f"--- Running ADF Test on raw '{target_col}' ---")
        # Handle potential edge case where series is constant
        if series.nunique() <= 1:
            print("[FAIL] Series is constant. Cannot test stationarity.")
            sys.exit(1)

        result = adfuller(series)
        p_value = result[1]
        print(f"ADF Statistic: {result[0]:.4f}")
        print(f"p-value: {p_value:.4f}")

        if p_value < significance_level:
            print("[PASS] Raw series is stationary.")
            sys.exit(0)  # Explicit success
        else:
            print("[FAIL] Raw series is Non-Stationary (Unit Root detected).")
            print("Recommendation: Apply differencing (e.g., df.diff()) or fractional differentiation.")

            # Run ADF on Differenced Series (Log Returns)
            print(f"\n--- Running ADF Test on Log Returns of '{target_col}' ---")

            # Log Return Calculation. Handle 0 or negative values in prices.
            if (series <= 0).any():
                print("[WARNING] Series contains non-positive values. Using simple pct_change instead of log returns.")
                returns = series.pct_change().dropna()
            else:
                returns = np.log(series / series.shift(1)).dropna()

            # Clean infinite values (e.g. if price jumped from 0, though caught above)
            returns = returns.replace([np.inf, -np.inf], np.nan).dropna()

            if returns.empty:
                print("[ERROR] Differencing resulted in empty series.")
                sys.exit(1)

            result_diff = adfuller(returns)
            p_value_diff = result_diff[1]
            print(f"ADF Statistic (Diff): {result_diff[0]:.4f}")
            print(f"p-value (Diff): {p_value_diff:.4f}")

            if p_value_diff < significance_level:
                print("[PASS] Differenced series is stationary. Use returns for modeling.")
                sys.exit(0)  # Explicit success
            else:
                print("[CRITICAL] Even differenced series is non-stationary. Check for structural breaks.")
                sys.exit(1)  # Fail the pipeline

    except Exception as e:
        print(f"[ERROR] Stationarity check failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_stationarity.py <path_to_data> [target_column]")
        sys.exit(1)

    target = sys.argv[2] if len(sys.argv) > 2 else 'close'
    validate_stationarity(sys.argv[1], target)