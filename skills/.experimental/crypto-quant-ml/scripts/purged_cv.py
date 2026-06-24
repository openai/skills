#!/usr/bin/env python3
import numpy as np
import pandas as pd
from sklearn.model_selection import KFold
import sys


class PurgedKFold:
    """
    Extended K-Fold class that implements Purging and Embargoing.
    """

    def __init__(self, n_splits=5, t1=None, pct_embargo=0.01):
        self.n_splits = n_splits
        self.t1 = t1
        self.pct_embargo = pct_embargo

        if self.t1 is None:
            raise ValueError("t1 (expiration times) must be provided for Purged K-Fold.")

    def split(self, X, y=None, groups=None):
        indices = np.arange(X.shape[0])
        n_samples = self.t1.shape[0]
        embargo = int(n_samples * self.pct_embargo)

        kf = KFold(n_splits=self.n_splits, shuffle=False)

        for train_idx, test_idx in kf.split(X):
            # Define Test Boundaries
            test_start_time = self.t1.index[test_idx[0]]

            # Use the max expiration time of the test set.
            # This ensures we don't start training until the last test trade has finished.
            test_max_endtime = self.t1.iloc[test_idx].max()

            train_start_times = self.t1.index[train_idx]
            train_end_times = self.t1.iloc[train_idx]

            # Mask A: Train ends before Test starts
            mask_before = train_end_times < test_start_time

            # Mask B: Train starts after Test ends (fully finished)
            mask_after = train_start_times > test_max_endtime

            # Handle both Series (has .values) and Numpy Arrays (no .values)
            # pd.Index comparison returns Numpy array; pd.Series comparison returns Series.
            if hasattr(mask_before, 'values'):
                mask_before = mask_before.values
            if hasattr(mask_after, 'values'):
                mask_after = mask_after.values

            train_indices_before = train_idx[mask_before]
            train_indices_after = train_idx[mask_after]

            # Apply Embargo
            if embargo > 0 and len(train_indices_after) > 0:
                train_indices_after = train_indices_after[embargo:]

            clean_train_idx = np.concatenate([train_indices_before, train_indices_after])

            yield clean_train_idx, test_idx


if __name__ == "__main__":
    print("--- Demonstrating Purged K-Fold ---")
    dates = pd.date_range(start='2023-01-01', periods=100, freq='D')

    # t1: Index = Trade Start, Value = Trade End (2 days later)
    t1 = pd.Series(dates + pd.Timedelta(days=2), index=dates)
    X = np.random.randn(100, 5)

    try:
        cv = PurgedKFold(n_splits=3, t1=t1, pct_embargo=0.01)

        fold = 1
        for train, test in cv.split(X):
            print(f"Fold {fold}: Train size {len(train)}, Test size {len(test)}")

            # Validation Logic Vectorized
            train_starts = t1.index[train]
            train_ends = t1.iloc[train]
            test_start = t1.index[test[0]]
            # Use .max() to handle variable durations (e.g. if the second-to-last sample is longer than the last)
            test_data_end = t1.iloc[test].max()

            # Create Boolean Mask of overlaps
            # Overlap exists if NOT (End_Train < Start_Test OR Start_Train > End_Test)
            # In pandas vector logic, 'or' becomes '|' and 'not' becomes '~'
            non_overlapping = (train_ends < test_start) | (train_starts > test_data_end)
            overlaps = ~non_overlapping

            if overlaps.any():
                print(f"[FAIL] Leakage detected! {overlaps.sum()} samples overlap.")
            else:
                print("[PASS] No overlap detected.")

            fold += 1
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)