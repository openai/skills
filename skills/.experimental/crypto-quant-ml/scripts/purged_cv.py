#!/usr/bin/env python3
import numpy as np
import pandas as pd
from sklearn.model_selection import KFold
import sys


class PurgedKFold:
    """
    Extended K-Fold class that implements Purging and Embargoing.
    citation: Lopez de Prado, Advances in Financial Machine Learning, Ch 7 "Cross-Validation in Finance"
    https://www.wiley.com/en-us/Advances+in+Financial+Machine+Learning-p-9781119482086
    """

    def __init__(self, n_splits=5, t1=None, pct_embargo=0.01):
        """
        :param n_splits: number of folds
        :param t1: pandas Series where index is the observation time (start) and value is the expiration time (end)
        :param pct_embargo: float, percentage of total data to embargo after test set
        """
        self.n_splits = n_splits
        self.t1 = t1  # Series of expiration times for each observation
        self.pct_embargo = pct_embargo

        if self.t1 is None:
            raise ValueError("t1 (expiration times) must be provided for Purged K-Fold.")

    def split(self, X, y=None, groups=None):
        indices = np.arange(X.shape[0])
        n_samples = self.t1.shape[0]
        embargo = int(n_samples * self.pct_embargo)

        kf = KFold(n_splits=self.n_splits, shuffle=False)

        for train_idx, test_idx in kf.split(X):
            # We assume t1.index aligns with X's rows 0..N
            test_start_time = self.t1.index[test_idx[0]]
            test_end_time = self.t1.index[test_idx[-1]]

            # Purging: Remove training samples that overlap with the test interval

            # Get times for all training candidates
            train_start_times = self.t1.index[train_idx]
            train_end_times = self.t1.iloc[train_idx]  # The values in t1 are the end times

            # Logic:
            # Drop samples where:
            # (Start_Train < End_Test) AND (End_Train > Start_Test)

            # Vectorized check for overlap
            # Overlap exists if the training sample's interval [start, end] touches [test_start, test_end]
            # Standard overlap logic: max(start1, start2) < min(end1, end2)

            # However, for purging specifically:
            # We want to KEEP samples that are strictly BEFORE test or strictly AFTER test.

            # Strictly Before: End_Train < Start_Test
            # Strictly After: Start_Train > End_Test

            # Mask for samples strictly before test
            # Note: We compare the *end time* of the training sample to the *start time* of the test block
            mask_before = train_end_times < test_start_time

            # Mask for samples strictly after test
            # Note: We compare the *start time* of the training sample to the *end time* of the test block
            mask_after = train_start_times > test_end_time

            # Apply masks to get indices
            train_indices_before = train_idx[mask_before]
            train_indices_after = train_idx[mask_after]

            # Embargoing: Drop a buffer period immediately after the test set
            # We only embargo the 'after' set because the 'before' set can't leak future info from the test set
            if embargo > 0 and len(train_indices_after) > 0:
                # We simply drop the first 'embargo' number of elements from the sorted 'after' set
                # valid because KFold (shuffle=False) preserves order
                train_indices_after = train_indices_after[embargo:]

            clean_train_idx = np.concatenate([train_indices_before, train_indices_after])

            yield clean_train_idx, test_idx


if __name__ == "__main__":
    # Demonstration on dummy data
    print("--- Demonstrating Purged K-Fold ---")
    dates = pd.date_range(start='2023-01-01', periods=100, freq='D')
    # t1 simulates a 'triple barrier' exit 2 days later
    # Index = Trade Start, Value = Trade End
    t1 = pd.Series(dates + pd.Timedelta(days=2), index=dates)
    X = np.random.randn(100, 5)

    try:
        cv = PurgedKFold(n_splits=3, t1=t1, pct_embargo=0.05)

        fold = 1
        for train, test in cv.split(X):
            print(f"Fold {fold}: Train size {len(train)}, Test size {len(test)}")
            # print(f"  Test range: {test[0]} to {test[-1]}")

            # Validation Logic
            train_starts = t1.index[train]
            train_ends = t1.iloc[train]
            test_start = t1.index[test[0]]
            test_end = t1.index[test[-1]]  # This is start time of last test sample
            # The actual "end of data used in test" is the end time of the last test sample
            test_data_end = t1.iloc[test[-1]]

            # Check overlap
            # A training sample overlaps if its [start, end] intersects with test [start, end]
            # More strictly for financial ML:
            # 1. No training label should result from data inside the test period.
            # 2. No test label should result from data inside the training period.

            # Check: Does any training interval overlap with the test interval (defined by widest bounds)?
            # Test interval strictly covers [test_start, test_data_end]

            overlaps = []
            for i in range(len(train)):
                ts = train_starts[i]
                te = train_ends[i]
                # Overlap condition: not (end < test_start or start > test_end)
                if not (te < test_start or ts > test_data_end):
                    overlaps.append(train[i])

            if overlaps:
                print(f"[FAIL] Leakage detected! {len(overlaps)} training samples overlap with test period.")
            else:
                print(f"[PASS] No overlap detected.")

            fold += 1
    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)