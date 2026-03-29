import os
from dotenv import load_dotenv
from fredapi import Fred
import pandas as pd

def fetch_gdp_data():
    load_dotenv()
    api_key = os.getenv('FRED_API_KEY')
    fred = Fred(api_key=api_key)
    data = fred.get_series('GDPC1')
    return pd.DataFrame(data, columns=['gdp_per_capita'])