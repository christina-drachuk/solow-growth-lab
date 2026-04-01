import os
from dotenv import load_dotenv
from fredapi import Fred
import pandas as pd
import wbgapi as wb
import streamlit as st

# Map of display names → ISO3 country codes for World Bank API
COUNTRY_MAP = {
    "United States": "USA",
    "United Kingdom": "GBR",
    "Japan": "JPN",
    "Germany": "DEU",
    "France": "FRA",
    "Canada": "CAN",
    "Australia": "AUS",
    "South Korea": "KOR",
    "China": "CHN",
    "India": "IND",
    "Brazil": "BRA",
    "Mexico": "MEX",
    "Italy": "ITA",
    "Spain": "ESP",
    "Sweden": "SWE",
    "Norway": "NOR",
    "Switzerland": "CHE",
    "Netherlands": "NLD",
    "South Africa": "ZAF",
    "Nigeria": "NGA",
    "Argentina": "ARG",
    "Turkey": "TUR",
    "Indonesia": "IDN",
    "Poland": "POL",
    "Chile": "CHL",
}

def fetch_gdp_data():
    """Fetch US Real GDP per Capita from FRED API (legacy function)."""
    load_dotenv()
    api_key = os.getenv('FRED_API_KEY')
    fred = Fred(api_key=api_key)
    data = fred.get_series('GDPC1')
    return pd.DataFrame(data, columns=['gdp_per_capita'])

@st.cache_data(ttl=3600)
def fetch_country_gdp(country_codes):
    """Fetch GDP per capita (constant 2015 US$) from World Bank for multiple countries.

    Parameters:
        country_codes (list): List of ISO3 country codes (e.g., ['USA', 'JPN', 'DEU'])

    Returns:
        pd.DataFrame: DataFrame with year index and one column per country (display name)
    """
    # NY.GDP.PCAP.KD = GDP per capita (constant 2015 US$)
    code_to_name = {v: k for k, v in COUNTRY_MAP.items()}

    data = wb.data.DataFrame('NY.GDP.PCAP.KD', economy=country_codes, time=range(1960, 2025))
    # wbgapi returns countries as rows and years as columns (YR1960, YR1961, ...)
    # Transpose so years are rows and countries are columns
    data = data.T

    # Clean year index: "YR1960" → 1960
    data.index = data.index.str.replace('YR', '').astype(int)
    data.index.name = 'Year'

    # Rename columns from ISO3 codes to display names
    data.columns = [code_to_name.get(c, c) for c in data.columns]

    data = data.sort_index()
    data = data.dropna(how='all')

    return data
