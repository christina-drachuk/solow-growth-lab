import numpy as np

def calculate_steady_state(s, n, g, delta, alpha):
    """Calculate the steady-state level of capital per worker.
    Parameters:
    s (float): Savings rate
    n (float): Population growth rate
    g (float): Technological growth rate
    delta (float): Depreciation rate
    alpha (float): Output elasticity of capital
    Returns:
    float: Steady-state level of capital per worker
    """
    denominator = n + g + delta
    exponent = 1 / (1 - alpha)

    k_star = (s / denominator) ** exponent
    return k_star

def calculate_output_per_worker(k_star, alpha):
    """Calculate the steady-state level of output per worker.
    Parameters:
    k_star (float): Steady-state level of capital per worker
    alpha (float): Output elasticity of capital
    Returns:
    float: Steady-state level of output per worker
    """
    y_star = k_star ** alpha
    return y_star

def derive_params(gdp_df):
    """
    Calculate the actual growth rate from FRED data.
    """

    gdp_df['gdp_growth_rate'] = gdp_df['gdp_per_capita'].pct_change()
    avg_g = gdp_df['gdp_growth_rate'].mean()
    return avg_g

if __name__ == "__main__":
    # Test with standard econ textbook values
    test_k = calculate_steady_state(s=0.2, n=0.02, g=0.02, delta=0.05, alpha=0.33)
    print(f"Calculated Steady State Capital: {test_k:.2f}")