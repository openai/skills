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
    """
    Dynamically imports a script as a module.
    Essential for testing scripts that reside outside the python package structure.
    """
    if not os.path.exists(path):
        pytest.fail(f"Script not found at: {path}")

    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# --- Setup Paths ---
# Assumes structure:
# /skill-root/
#    /scripts/
#    /tests/test_validation_scripts.py
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(BASE_DIR, 'scripts')

# Import modules
validate_stationarity = import_script('validate_stationarity', os.path.join(SCRIPTS_DIR, 'validate_stationarity.py'))
purged_cv = import_script('purged_cv', os.path.join(SCRIPTS_DIR, 'purged_cv.py'))
detect_leakage = import_script('detect_leakage', os.path.join(SCRIPTS_DIR, 'detect_leakage.py'))


# --- Tests for validate_stationarity.py ---

@pytest.fixture
def stationary_series():
    # Generate white noise (stationary)
    np.random.seed(42)
    return pd.Series(np.random.randn(100), name='close')


@pytest.fixture
def non_stationary_series():
    # Generate a random walk (non-stationary)
    np.random.seed(42)
    return pd.Series(np.random.randn(100).cumsum(), name='close')


def test_stationarity_pass(tmp_path, stationary_series):
    """Test that a stationary series passes the validation (Exit Code 0)."""
    df = pd.DataFrame(stationary_series)
    f = tmp_path / "stationary.csv"
    df.to_csv(f)

    with patch('sys.stdout', new=StringIO()) as fake_out:
        # Expect SystemExit(0) for success
        with pytest.raises(SystemExit) as e:
            validate_stationarity.validate_stationarity(str(f), 'close')

        assert e.value.code == 0
        assert "[PASS] Raw series is stationary" in fake_out.getvalue()


def test_stationarity_fail_then_pass_diff(tmp_path, non_stationary_series):
    """Test that a non-stationary series fails raw check but passes on differencing (Exit Code 0)."""
    df = pd.DataFrame(non_stationary_series)
    f = tmp_path / "non_stationary.csv"
    df.to_csv(f)

    with patch('sys.stdout', new=StringIO()) as fake_out:
        # Expect SystemExit(0) eventually
        with pytest.raises(SystemExit) as e:
            validate_stationarity.validate_stationarity(str(f), 'close')

        assert e.value.code == 0
        output = fake_out.getvalue()
        assert "[FAIL] Raw series is Non-Stationary" in output
        assert "[PASS] Differenced series is stationary" in output


# --- Tests for purged_cv.py ---

def test_purged_kfold_no_overlap():
    """Test that PurgedKFold generates splits without overlap between train and test."""
    n_samples = 50
    dates = pd.date_range(start='2023-01-01', periods=n_samples, freq='D')
    # t1 (expiration) is 2 days after the observation
    t1 = pd.Series(dates + pd.Timedelta(days=2), index=dates)
    X = np.random.randn(n_samples, 2)

    cv = purged_cv.PurgedKFold(n_splits=3, t1=t1, pct_embargo=0.0)

    for train_idx, test_idx in cv.split(X):
        # Get the times for train and test sets
        train_times = t1.index[train_idx]
        test_start = t1.index[test_idx[0]]
        test_end = t1.index[test_idx[-1]]

        # Check for overlap:
        # Overlap exists if any training time is inside the [test_start, test_end] interval
        overlap = any((train_times >= test_start) & (train_times <= test_end))
        assert not overlap, f"Found training samples overlapping with test range {test_start}-{test_end}"


def test_purged_kfold_embargo():
    """Test that embargo properly drops samples after the test set."""
    n_samples = 100
    dates = pd.date_range(start='2023-01-01', periods=n_samples, freq='D')
    t1 = pd.Series(dates + pd.Timedelta(days=1), index=dates)
    X = np.random.randn(n_samples, 2)

    # 10% embargo -> should drop 10 samples after test set
    cv = purged_cv.PurgedKFold(n_splits=2, t1=t1, pct_embargo=0.10)

    splits = list(cv.split(X))
    # Test fold 0: Test set is usually the first chunk.
    train_idx, test_idx = splits[0]

    test_last_idx = test_idx[-1]

    # Identify the immediate next samples that SHOULD be embargoed
    embargoed_indices = np.arange(test_last_idx + 1, test_last_idx + 11)

    # Ensure these are NOT in train_idx
    intersection = np.intersect1d(train_idx, embargoed_indices)
    assert len(intersection) == 0, f"Embargo failed. Found embargoed indices {intersection} in training set."


# --- Tests for detect_leakage.py ---

def test_leakage_detection_pass(tmp_path):
    """Test that a dataset with low correlations passes (Exit Code 0)."""
    df = pd.DataFrame({
        'feature1': np.random.randn(100),
        'feature2': np.random.randn(100),
        'target': np.random.randn(100)
    })
    f = tmp_path / "clean_data.csv"
    df.to_csv(f, index=False)

    with patch('sys.stdout', new=StringIO()) as fake_out:
        with pytest.raises(SystemExit) as e:
            detect_leakage.detect_leakage(str(f), 'target')

        assert e.value.code == 0
        assert "[PASS]" in fake_out.getvalue()


def test_leakage_detection_fail(tmp_path):
    """Test that a dataset with perfect correlation fails (Exit Code 1)."""
    target = np.random.randn(100)
    df = pd.DataFrame({
        'feature1': target,  # Perfect leakage
        'feature2': np.random.randn(100),
        'target': target
    })
    f = tmp_path / "leaky_data.csv"
    df.to_csv(f, index=False)

    with patch('sys.stdout', new=StringIO()) as fake_out:
        # Expect sys.exit(1)
        with pytest.raises(SystemExit) as e:
            detect_leakage.detect_leakage(str(f), 'target')

        assert e.value.code == 1

        output = fake_out.getvalue()
        assert "[WARNING]" in output
        assert "feature1" in output  # Should identify the leaky feature


def test_leakage_detection_infer_target(tmp_path):
    """Test that the script correctly infers the target column if not provided (Exit Code 0)."""
    df = pd.DataFrame({
        'feature1': np.random.randn(100),
        'my_target_label': np.random.randn(100)
    })
    f = tmp_path / "inferred_target.csv"
    df.to_csv(f, index=False)

    with patch('sys.stdout', new=StringIO()) as fake_out:
        # Pass a dummy target name that doesn't exist so it tries to infer
        with pytest.raises(SystemExit) as e:
            detect_leakage.detect_leakage(str(f), 'non_existent')

        assert e.value.code == 0
        assert "Inferred target column: my_target_label" in fake_out.getvalue()