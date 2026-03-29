import os
import streamlit as st
import plotly.express as px
from data_fetch import fetch_gdp_data
from solow_model import calculate_steady_state
import google.generativeai as genai

# Page config
st.set_page_config(page_title="Solow Growth Lab", layout="wide")
st.title("📈 The Interactive Solow Growth Lab")

# --- Sidebar: User Controls ---
st.sidebar.header("Adjust Model Parameters")
s = st.sidebar.slider("Savings Rate (s)", 0.05, 0.50, 0.20, help="Percent of income saved/invested")
n = st.sidebar.slider("Population Growth (n)", 0.0, 0.05, 0.01)
delta = st.sidebar.slider("Depreciation (δ)", 0.01, 0.10, 0.05)
alpha = st.sidebar.slider("Capital Share (α)", 0.20, 0.50, 0.33)

# --- Data Logic ---
df = fetch_gdp_data()

def get_ai_insight(s, n, g, delta, k_star):
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('models/gemini-flash-latest')
    
    prompt = f"""
    Act as a Quantitative Economist. I have a Solow Growth Model with these parameters:
    Savings Rate (s): {s}, Population Growth (n): {n}, Tech Growth (g): {g}, Depreciation (delta): {delta}.
    The calculated Steady State Capital (k*) is {k_star:.2f}.
    
    In 3 concise bullet points, explain what this means for the long-term 
    economic health of a country with these specific numbers.
    """
    response = model.generate_content(prompt)
    return response.text

if df is not None:
    # Calculate the Steady State based on user sliders
    # We'll assume a constant tech growth (g) of 2% for this demo
    k_star = calculate_steady_state(s, n, 0.02, delta, alpha)
    y_star = k_star ** alpha # Steady state output
    
    # --- Visualization: The "Hover" Graph ---
    st.subheader("Real GDP per Capita Over Time")
    
    # Create a Plotly chart (This provides the hover interaction)
    fig = px.line(df, x=df.index, y='gdp_per_capita', 
                  title="U.S. Growth Trajectory",
                  labels={'gdp_per_capita': 'GDP per Capita ($)', 'index': 'Date'})
    
    # Customizing the Hover Look
    fig.update_traces(mode="lines", hovertemplate="<b>Date:</b> %{x}<br><b>Income:</b> $%{y:,.0f}")
    
    # Add a horizontal line for our "Theoretical Steady State"
    # Note: In a real model, y* is a ratio, but we scale it here for visual comparison
    fig.add_hline(y=y_star * 15000, line_dash="dash", line_color="red", 
                  annotation_text=f"Theoretical Steady State: ${y_star*15000:,.0f}")

    st.plotly_chart(fig, use_container_width=True)

    # --- Analysis Metrics ---
    col1, col2 = st.columns(2)
    col1.metric("Current Parameter k*", f"{k_star:.2f}")
    col2.metric("Implied Steady State y*", f"${y_star*15000:,.0f}")

with st.expander("View the Math Behind the Model"):
    st.latex(r'''
        k^* = \left( \frac{s}{n + g + \delta} \right)^{\frac{1}{1-\alpha}}
    ''')
    st.write("This equation represents the steady-state capital per effective worker...")

st.divider()
st.subheader("🤖 AI Economic Analyst")
if st.button("Generate Model Insights"):
    with st.spinner("Analyzing parameters..."):
        insight = get_ai_insight(s, n, 0.02, delta, k_star)
        st.info(insight)