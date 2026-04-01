import pytest
import pandas as pd
import numpy as np


@pytest.fixture
def standard_params():
    """Standard macroeconomics textbook Solow model parameters."""
    return {
        "s": 0.20,      # savings rate
        "n": 0.02,      # population growth rate
        "g": 0.02,      # technological growth rate
        "delta": 0.05,   # depreciation rate
        "alpha": 0.33,   # capital share (output elasticity)
    }


@pytest.fixture
def sample_gdp_df():
    """Realistic GDP-per-capita DataFrame for derive_params testing."""
    years = pd.date_range("2000", periods=5, freq="YE")
    # GDP growing at ~3% per year: 50000 → 51500 → 53045 → 54636 → 56275
    values = [50000, 51500, 53045, 54636, 56275]
    return pd.DataFrame({"gdp_per_capita": values}, index=years)


@pytest.fixture
def mock_wb_raw_response():
    """DataFrame mimicking raw wbgapi.data.DataFrame output.

    wbgapi returns countries as rows indexed by ISO3 codes
    and years as columns prefixed with 'YR' (e.g. YR2020).
    """
    data = {
        "YR2020": [63000.0, 40000.0],
        "YR2021": [65000.0, 41000.0],
        "YR2022": [67000.0, 42000.0],
    }
    return pd.DataFrame(data, index=["USA", "JPN"])
