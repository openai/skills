import pytest
import pandas as pd
import numpy as np
import sys
import os
import importlib.util
from io import StringIO
from unittest.mock import patch


# --- Helper to Import Scripts Dynamically ---
def import_script(name, path):
    if not os.path.exists(path):
        pytest.fail(f"Script not found at: {path}")
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# --- Setup Paths ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(BASE_DIR, 'scripts')

# Import modules
validate_stationarity = import_script('validate_stationarity', os.path.join(SCRIPTS_DIR, 'validate_stationarity.py'))
purged_cv = import_script('purged_cv', os.path.join(SCRIPTS_DIR, 'purged_cv.py'))
detect_leakage = import_script('detect_leakage', os.path.join(SCRIPTS_DIR, 'detect_leakage.py'))


# --- Tests for validate_stationarity.py ---

@pytest.fixture
def stationary_series():
    np.random.seed(42)
    return pd.Series(np.random.randn(100), name='close')


@pytest.fixture
def non_stationary_series():
    np.random.seed(42)
    return pd.Series(np.random.randn(100).cumsum(), name='close')


def test_stationarity_pass(tmp_path, stationary_series):
    """Test that a stationary series passes (Returns True)."""
    df = pd.DataFrame(stationary_series)
    f = tmp_path / "stationary.csv"
    df.to_csv(f)

    with patch('sys.stdout', new=StringIO()) as fake_out:
        result = validate_stationarity.validate_stationarity(str(f), 'close')
        assert result is True
        assert "[PASS] Raw series is stationary" in fake_out.getvalue()


def test_stationarity_fail_then_pass_diff(tmp_path, non_stationary_series):
    """Test that a non-stationary series passes on differencing (Returns True)."""
    df = pd.DataFrame(non_stationary_series)
    f = tmp_path / "non_stationary.csv"
    df.to_csv(f)

    with patch('sys.stdout', new=StringIO()) as fake_out:
        result = validate_stationarity.validate_stationarity(str(f), 'close')
        assert result is True
        output = fake_out.getvalue()
        assert "[FAIL] Raw series is Non-Stationary" in output
        assert "[PASS] Differenced series is stationary" in output


# --- Tests for purged_cv.py ---

def test_purged_kfold_no_overlap():
    """
    Test that PurgedKFold properly purges samples based on TIME overlap, not just Index.
    """
    n_samples = 50
    dates = pd.date_range(start='2023-01-01', periods=n_samples, freq='D')

    # Create Long Durations (3 days) to force overlap if purging isn't working
    # e.g., A trade on Jan 1st ends Jan 4th. If Test starts Jan 3rd, this MUST be purged.
    t1 = pd.Series(dates + pd.Timedelta(days=3), index=dates)
    X = np.random.randn(n_samples, 2)

    cv = purged_cv.PurgedKFold(n_splits=3, t1=t1, pct_embargo=0.0)

    for train_idx, test_idx in cv.split(X):
        train_starts = t1.index[train_idx]
        train_ends = t1.iloc[train_idx]

        test_start = t1.index[test_idx[0]]
        test_max_end = t1.iloc[test_idx].max()

        # Overlap exists if: (Train_Start < Test_End) AND (Train_End > Test_Start)
        # This covers both "front-running" the test set and "trailing" into the test set.

        # Train samples that end inside (or after) the test start
        leakage_mask = (train_ends > test_start) & (train_starts < test_max_end)

        n_leakage = leakage_mask.sum()
        assert n_leakage == 0, f"Found {n_leakage} training samples overlapping with test range {test_start} to {test_max_end}"


def test_purged_kfold_embargo():
    """Test that embargo properly drops samples after the test set."""
    n_samples = 100
    dates = pd.date_range(start='2023-01-01', periods=n_samples, freq='D')
    t1 = pd.Series(dates + pd.Timedelta(days=1), index=dates)
    X = np.random.randn(n_samples, 2)

    cv = purged_cv.PurgedKFold(n_splits=2, t1=t1, pct_embargo=0.10)
    splits = list(cv.split(X))
    train_idx, test_idx = splits[0]
    test_last_idx = test_idx[-1]

    # Check the 10 samples immediately following the test set
    embargoed_indices = np.arange(test_last_idx + 1, test_last_idx + 11)
    intersection = np.intersect1d(train_idx, embargoed_indices)
    assert len(intersection) == 0, f"Embargo failed. Found {intersection} in training set."


# --- Tests for detect_leakage.py ---

def test_leakage_detection_pass(tmp_path):
    """Test that a dataset with low correlations passes (Returns True)."""
    df = pd.DataFrame({
        'feature1': np.random.randn(100),
        'feature2': np.random.randn(100),
        'target': np.random.randn(100)
    })
    f = tmp_path / "clean_data.csv"
    df.to_csv(f, index=False)

    with patch('sys.stdout', new=StringIO()) as fake_out:
        result = detect_leakage.detect_leakage(str(f), 'target')
        assert result is True
        assert "[PASS]" in fake_out.getvalue()


def test_leakage_detection_fail(tmp_path):
    """Test that a dataset with perfect correlation fails (Returns False)."""
    target = np.random.randn(100)
    df = pd.DataFrame({
        'feature1': target,  # Perfect leakage
        'feature2': np.random.randn(100),
        'target': target
    })
    f = tmp_path / "leaky_data.csv"
    df.to_csv(f, index=False)

    with patch('sys.stdout', new=StringIO()) as fake_out:
        result = detect_leakage.detect_leakage(str(f), 'target')
        assert result is False
        assert "[WARNING]" in fake_out.getvalue()
        assert "feature1" in fake_out.getvalue()


def test_leakage_detection_infer_target(tmp_path):
    """Test target inference (Returns True)."""
    df = pd.DataFrame({
        'feature1': np.random.randn(100),
        'my_target_label': np.random.randn(100)
    })
    f = tmp_path / "inferred_target.csv"
    df.to_csv(f, index=False)

    with patch('sys.stdout', new=StringIO()) as fake_out:
        result = detect_leakage.detect_leakage(str(f), target_col=None)

        assert result is True
        # FIX: Added single quotes to match script output
        assert "Inferred target column: 'my_target_label'" in fake_out.getvalue()