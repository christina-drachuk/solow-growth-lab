from solow_growth.data_fetch import fetch_gdp_data
from solow_growth.solow_model import calculate_steady_state, derive_params

def run_analysis():
    print("Fetching real-world data...")
    df = fetch_gdp_data()

    g_real = derive_params(df)
    print(f"Derived real growth rate from FRED data: {g_real:.4f}")

    k_star_real = calculate_steady_state(s=0.2, n=0.01, g=g_real, delta=0.05, alpha=0.33)
    print(f"Based on real GDP growth, Theoretical Steady State (k*) is {k_star_real:.2f}")

if __name__ == "__main__":
    run_analysis()
