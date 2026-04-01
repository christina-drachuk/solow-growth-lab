"""Tests for main.py — CLI analysis (external calls mocked)."""

from unittest.mock import patch, MagicMock
import pandas as pd
import pytest

from solow_growth.main import run_analysis


class TestRunAnalysis:
    """Tests for the CLI analysis entry point."""

    @patch("solow_growth.main.fetch_gdp_data")
    @patch("solow_growth.main.derive_params")
    @patch("solow_growth.main.calculate_steady_state")
    def test_calls_steady_state_with_derived_g(
        self, mock_steady_state, mock_derive, mock_fetch
    ):
        """Should pass the empirically derived g into calculate_steady_state."""
        mock_fetch.return_value = pd.DataFrame({"gdp_per_capita": [50000, 51500]})
        mock_derive.return_value = 0.03
        mock_steady_state.return_value = 4.0

        run_analysis()

        mock_steady_state.assert_called_once_with(
            s=0.2, n=0.01, g=0.03, delta=0.05, alpha=0.33
        )

    @patch("solow_growth.main.fetch_gdp_data")
    @patch("solow_growth.main.derive_params")
    @patch("solow_growth.main.calculate_steady_state")
    def test_prints_results(self, mock_steady_state, mock_derive, mock_fetch, capsys):
        """Should print derived growth rate and steady-state capital."""
        mock_fetch.return_value = pd.DataFrame({"gdp_per_capita": [50000, 51500]})
        mock_derive.return_value = 0.03
        mock_steady_state.return_value = 4.0

        run_analysis()

        captured = capsys.readouterr()
        assert "0.03" in captured.out or "0.0300" in captured.out
        assert "4.00" in captured.out
