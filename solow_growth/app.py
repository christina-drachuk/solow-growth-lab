import os
from dotenv import load_dotenv
import streamlit as st
import plotly.graph_objects as go
from solow_growth.data_fetch import fetch_country_gdp, COUNTRY_MAP
from solow_growth.solow_model import calculate_steady_state
import google.generativeai as genai

load_dotenv()


def get_ai_insight(s, n, g, delta, k_star, countries):
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('models/gemini-flash-latest')

    prompt = f"""
    Act as a Quantitative Economist. I have a Solow Growth Model with these parameters:
    Savings Rate (s): {s}, Population Growth (n): {n}, Tech Growth (g): {g}, Depreciation (delta): {delta}.
    The calculated Steady State Capital (k*) is {k_star:.2f}.

    I am comparing the following countries: {', '.join(countries)}.

    In 3-4 concise bullet points:
    1. Explain what this steady state means for long-term economic health.
    2. Comment on how the selected countries compare against the theoretical prediction.
    3. Note any interesting divergences between these economies.
    """
    response = model.generate_content(prompt)
    return response.text


def main():
    # Page config
    st.set_page_config(page_title="Solow Growth Lab", layout="wide")
    st.title("📈 The Interactive Solow Growth Lab")

    # --- Sidebar: About the Model ---
    with st.sidebar.expander("About the Solow Growth Model"):
        st.markdown(
            """
            The **Solow Growth Model** (1956) is one of the foundational models in
            macroeconomics. It explains long-run economic growth by looking at how
            **capital accumulation**, **labor force growth**, and **technological
            progress** interact over time.

            The key insight is that economies converge toward a **steady state** — a
            long-run equilibrium where capital per worker and output per worker stop
            growing (absent technological change). Countries with higher savings rates
            accumulate more capital and reach higher steady-state income levels, while
            faster population growth dilutes capital across more workers, lowering
            the steady state.

            Use the sliders below to adjust the model parameters and see how the
            theoretical steady state compares against real GDP data.
            """
        )

    # --- Sidebar: Country Selection ---
    st.sidebar.header("Select Countries")
    available_countries = sorted(COUNTRY_MAP.keys())
    selected_countries = st.sidebar.multiselect(
        "Choose countries to compare (2-5)",
        options=available_countries,
        default=["United States", "Japan", "Germany"],
        max_selections=5,
    )

    # --- Sidebar: Model Parameters ---
    st.sidebar.header("Adjust Model Parameters")
    s = st.sidebar.slider("Savings Rate (s)", 0.05, 0.50, 0.20, help="Percent of income saved/invested")
    n = st.sidebar.slider("Population Growth (n)", 0.0, 0.05, 0.01)
    delta = st.sidebar.slider("Depreciation (δ)", 0.01, 0.10, 0.05)
    alpha = st.sidebar.slider("Capital Share (α)", 0.20, 0.50, 0.33)

    # --- Data Logic ---
    # Calculate steady state from sliders (always available, even without countries)
    k_star = calculate_steady_state(s, n, 0.02, delta, alpha)
    y_star = k_star ** alpha  # Steady state output per effective worker
    steady_state_value = y_star * 15000  # Scaled for dollar comparison

    if not selected_countries:
        st.warning("Please select at least one country to see GDP comparisons.")
    else:
        country_codes = [COUNTRY_MAP[name] for name in selected_countries]
        try:
            df = fetch_country_gdp(country_codes)
        except Exception as e:
            st.error(f"Could not fetch GDP data: {e}")
            df = None

        if df is not None and not df.empty:
            # --- Visualization: Multi-Country GDP Comparison ---
            st.subheader("Real GDP per Capita Over Time")

            fig = go.Figure()

            # Add a line for each selected country
            for country in df.columns:
                series = df[country].dropna()
                fig.add_trace(go.Scatter(
                    x=series.index,
                    y=series.values,
                    mode='lines',
                    name=country,
                    hovertemplate=f"<b>{country}</b><br>Year: %{{x}}<br>GDP/Capita: $%{{y:,.0f}}<extra></extra>"
                ))

            # Add steady-state horizontal line
            # Note: y* is a ratio scaled by 15000 for visual comparison with real dollar values
            fig.add_hline(
                y=steady_state_value, line_dash="dash", line_color="red",
                annotation_text=f"Theoretical Steady State: ${steady_state_value:,.0f}"
            )

            fig.update_layout(
                title="GDP per Capita Comparison (constant 2015 US$)",
                xaxis_title="Year",
                yaxis_title="GDP per Capita ($)",
                hovermode="x unified",
                legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
            )

            st.plotly_chart(fig, width='stretch')

            # --- Analysis Metrics ---
            col1, col2 = st.columns(2)
            col1.metric("Steady State Capital (k*)", f"{k_star:.2f}")
            col2.metric("Implied Steady State Output (y*)", f"${steady_state_value:,.0f}")

            # Show latest GDP for each country
            st.subheader("Latest GDP per Capita by Country")
            latest_cols = st.columns(min(len(selected_countries), 5))
            for i, country in enumerate(df.columns):
                latest_value = df[country].dropna().iloc[-1] if not df[country].dropna().empty else None
                if latest_value is not None:
                    latest_cols[i].metric(country, f"${latest_value:,.0f}")

    with st.expander("View the Math Behind the Model"):
        st.latex(r'''
            k^* = \left( \frac{s}{n + g + \delta} \right)^{\frac{1}{1-\alpha}}
        ''')
        st.markdown(
            """
            This equation gives the **steady-state capital per effective worker** —
            the long-run level of capital the economy converges to.

            | Symbol | Name | Role in the Model |
            |--------|------|--------------------|
            | **s** | Savings Rate | Share of output invested in new capital. Higher savings → more capital accumulation → higher steady state. |
            | **n** | Population Growth | Rate at which the labor force expands. More workers means existing capital is spread thinner, lowering capital per worker. |
            | **g** | Technological Growth | Rate of productivity improvement (fixed at 2% in this demo). Drives sustained per-capita income growth beyond the steady state. |
            | **δ** | Depreciation | Fraction of capital that wears out each period. Higher depreciation erodes the capital stock faster, reducing the steady state. |
            | **α** | Capital Share | Output elasticity of capital (typically ~⅓). Governs diminishing returns — higher α means capital is more productive and the steady state is higher. |

            **Derived quantities:**
            - **k*** (steady-state capital per effective worker) — the level shown in the formula above.
            - **y*** = (k*)^α — steady-state output per effective worker, scaled by ×15,000 on the chart to compare with real GDP in dollars.
            """
        )

    st.divider()
    st.subheader("🤖 AI Economic Analyst")
    if not selected_countries:
        st.info("Select at least one country to generate AI insights.")
    elif st.button("Generate Model Insights"):
        with st.spinner("Analyzing parameters..."):
            insight = get_ai_insight(s, n, 0.02, delta, k_star, selected_countries)
            st.info(insight)
