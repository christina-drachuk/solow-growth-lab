"""Tests for solow_model.py — pure mathematical functions.

All expected values are hand-calculable from the Solow steady-state formula:
    k* = (s / (n + g + δ))^(1 / (1 − α))
    y* = (k*)^α
"""

import math
import numpy as np
import pandas as pd
import pytest

from solow_growth.solow_model import calculate_steady_state, calculate_output_per_worker, derive_params


# ── calculate_steady_state ──────────────────────────────────────────────


class TestCalculateSteadyState:
    """Tests for the core steady-state capital formula."""

    def test_textbook_values(self, standard_params):
        """Standard econ textbook values should yield k* ≈ 3.293."""
        k_star = calculate_steady_state(**standard_params)
        # Hand calc: (0.20 / (0.02 + 0.02 + 0.05))^(1/(1-0.33))
        #          = (2.2222...)^(1.4925...)
        #          ≈ 3.293
        assert k_star == pytest.approx(3.293, abs=0.01)

    def test_higher_savings_increases_k_star(self, standard_params):
        """Higher savings rate should yield a higher steady-state capital."""
        k_low = calculate_steady_state(**standard_params)
        params_high_s = {**standard_params, "s": 0.40}
        k_high = calculate_steady_state(**params_high_s)
        assert k_high > k_low

    def test_higher_depreciation_decreases_k_star(self, standard_params):
        """Higher depreciation should lower steady-state capital."""
        k_base = calculate_steady_state(**standard_params)
        params_high_delta = {**standard_params, "delta": 0.10}
        k_depre = calculate_steady_state(**params_high_delta)
        assert k_depre < k_base

    def test_zero_population_and_tech_growth(self):
        """n=0 and g=0 should still compute a valid k*."""
        k_star = calculate_steady_state(s=0.20, n=0.0, g=0.0, delta=0.05, alpha=0.33)
        # (0.20 / 0.05)^(1/(1-0.33)) = 4^(1.4925...) ≈ 7.918
        assert k_star == pytest.approx(7.918, abs=0.01)
        assert math.isfinite(k_star)

    def test_alpha_sensitivity(self, standard_params):
        """Higher α (capital share) should increase k* (slower diminishing returns)."""
        k_low_alpha = calculate_steady_state(**{**standard_params, "alpha": 0.25})
        k_high_alpha = calculate_steady_state(**{**standard_params, "alpha": 0.45})
        assert k_high_alpha > k_low_alpha

    def test_result_is_positive(self, standard_params):
        """Steady-state capital must always be positive with valid inputs."""
        k_star = calculate_steady_state(**standard_params)
        assert k_star > 0

    def test_symmetric_n_and_g(self):
        """n and g enter the formula identically; swapping them should give the same result."""
        k1 = calculate_steady_state(s=0.20, n=0.01, g=0.03, delta=0.05, alpha=0.33)
        k2 = calculate_steady_state(s=0.20, n=0.03, g=0.01, delta=0.05, alpha=0.33)
        assert k1 == pytest.approx(k2)


# ── calculate_output_per_worker ─────────────────────────────────────────


class TestCalculateOutputPerWorker:
    """Tests for the output-per-effective-worker function y* = (k*)^α."""

    def test_known_pair(self):
        """k*=3.07, α=0.33 → y* ≈ 1.44."""
        y_star = calculate_output_per_worker(3.07, 0.33)
        assert y_star == pytest.approx(1.44, abs=0.02)

    def test_identity_k_star_one(self):
        """k*=1 → y*=1 for any α."""
        for alpha in [0.20, 0.33, 0.50, 0.80]:
            assert calculate_output_per_worker(1.0, alpha) == pytest.approx(1.0)

    def test_monotonicity(self):
        """Higher k* should always produce higher y*."""
        y1 = calculate_output_per_worker(2.0, 0.33)
        y2 = calculate_output_per_worker(5.0, 0.33)
        assert y2 > y1

    def test_result_positive(self):
        """Output must be positive for positive capital."""
        assert calculate_output_per_worker(10.0, 0.33) > 0


# ── derive_params ───────────────────────────────────────────────────────


class TestDeriveParams:
    """Tests for empirical growth-rate derivation from GDP data."""

    def test_known_growth_rate(self, sample_gdp_df):
        """Derived g should match the mean of percentage changes (~3%)."""
        g = derive_params(sample_gdp_df)
        assert g == pytest.approx(0.03, abs=0.002)

    def test_constant_gdp_returns_zero(self):
        """If GDP is constant over time, growth rate should be 0."""
        df = pd.DataFrame({"gdp_per_capita": [50000, 50000, 50000, 50000]})
        g = derive_params(df)
        assert g == pytest.approx(0.0)

    def test_single_row_returns_nan(self):
        """A single data point cannot compute a growth rate; should return NaN."""
        df = pd.DataFrame({"gdp_per_capita": [50000]})
        g = derive_params(df)
        assert np.isnan(g)
