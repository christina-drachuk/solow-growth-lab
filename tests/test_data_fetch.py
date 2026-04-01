"""Tests for data_fetch.py — API integration layer (all external calls mocked)."""

from unittest.mock import patch, MagicMock
import pandas as pd
import pytest

from solow_growth.data_fetch import COUNTRY_MAP, fetch_gdp_data, fetch_country_gdp


# ── COUNTRY_MAP ─────────────────────────────────────────────────────────


class TestCountryMap:
    """Validate the country code mapping dictionary."""

    def test_has_25_entries(self):
        assert len(COUNTRY_MAP) == 25

    def test_known_mappings(self):
        assert COUNTRY_MAP["United States"] == "USA"
        assert COUNTRY_MAP["Japan"] == "JPN"
        assert COUNTRY_MAP["Germany"] == "DEU"
        assert COUNTRY_MAP["United Kingdom"] == "GBR"

    def test_all_codes_are_three_letter(self):
        for name, code in COUNTRY_MAP.items():
            assert len(code) == 3, f"{name} has code '{code}' which is not 3 characters"

    def test_all_codes_uppercase(self):
        for name, code in COUNTRY_MAP.items():
            assert code == code.upper(), f"{name} has code '{code}' which is not uppercase"


# ── fetch_gdp_data (FRED) ──────────────────────────────────────────────


class TestFetchGdpData:
    """Tests for the legacy FRED-based GDP fetch function."""

    @patch("solow_growth.data_fetch.Fred")
    @patch("solow_growth.data_fetch.load_dotenv")
    def test_returns_dataframe_with_correct_column(self, mock_dotenv, mock_fred_cls):
        """Returned DataFrame should have a 'gdp_per_capita' column."""
        mock_fred = MagicMock()
        mock_fred.get_series.return_value = pd.Series(
            [50000, 51000, 52000],
            index=pd.date_range("2020", periods=3, freq="YE"),
        )
        mock_fred_cls.return_value = mock_fred

        df = fetch_gdp_data()

        assert isinstance(df, pd.DataFrame)
        assert "gdp_per_capita" in df.columns
        assert len(df) == 3

    @patch("solow_growth.data_fetch.Fred")
    @patch("solow_growth.data_fetch.load_dotenv")
    def test_calls_fred_with_gdpc1(self, mock_dotenv, mock_fred_cls):
        """Should fetch the GDPC1 series from FRED."""
        mock_fred = MagicMock()
        mock_fred.get_series.return_value = pd.Series([50000])
        mock_fred_cls.return_value = mock_fred

        fetch_gdp_data()

        mock_fred.get_series.assert_called_once_with("GDPC1")


# ── fetch_country_gdp (World Bank) ─────────────────────────────────────


class TestFetchCountryGdp:
    """Tests for the World Bank multi-country GDP fetch function."""

    @patch("solow_growth.data_fetch.wb")
    def test_year_index_cleaned(self, mock_wb, mock_wb_raw_response):
        """Year index should be integers (not 'YR'-prefixed strings)."""
        mock_wb.data.DataFrame.return_value = mock_wb_raw_response

        # Clear Streamlit cache for testing
        fetch_country_gdp.clear()
        df = fetch_country_gdp(["USA", "JPN"])

        assert df.index.dtype in (int, "int64", "int32")
        assert list(df.index) == [2020, 2021, 2022]

    @patch("solow_growth.data_fetch.wb")
    def test_columns_renamed_to_display_names(self, mock_wb, mock_wb_raw_response):
        """Columns should use display names (not ISO3 codes)."""
        mock_wb.data.DataFrame.return_value = mock_wb_raw_response

        fetch_country_gdp.clear()
        df = fetch_country_gdp(["USA", "JPN"])

        assert "United States" in df.columns
        assert "Japan" in df.columns
        assert "USA" not in df.columns

    @patch("solow_growth.data_fetch.wb")
    def test_sorted_by_year(self, mock_wb):
        """Results should be sorted by year ascending."""
        raw = pd.DataFrame(
            {"YR2022": [67000.0], "YR2020": [63000.0], "YR2021": [65000.0]},
            index=["USA"],
        )
        mock_wb.data.DataFrame.return_value = raw

        fetch_country_gdp.clear()
        df = fetch_country_gdp(["USA"])

        assert list(df.index) == [2020, 2021, 2022]

    @patch("solow_growth.data_fetch.wb")
    def test_drops_all_nan_rows(self, mock_wb):
        """Rows where every column is NaN should be dropped."""
        raw = pd.DataFrame(
            {
                "YR2020": [63000.0],
                "YR2021": [float("nan")],
                "YR2022": [67000.0],
            },
            index=["USA"],
        )
        mock_wb.data.DataFrame.return_value = raw

        fetch_country_gdp.clear()
        df = fetch_country_gdp(["USA"])

        assert 2021 not in df.index
        assert len(df) == 2
