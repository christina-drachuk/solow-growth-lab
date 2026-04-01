# 📈 Interactive Solow Growth Lab
**An AI-Co-piloted Economic Analysis Tool**

## 🎯 Overview
An interactive web application that bridges **Neoclassical Growth Theory** with **Real-World Data**. Compare GDP per capita across **25 countries** using World Bank data, manipulate Solow Growth Model parameters, and visualize how theoretical steady states align with historical economic performance.

## 🚀 Key Features
* **Multi-Country Comparison:** GDP per capita data for 25 countries via the World Bank API (constant 2015 US$, 1960–present).
* **Interactive Modeling:** Dynamic Plotly visualizations that respond to parameter shifts (Savings, Population Growth, Depreciation, Capital Share).
* **AI-Powered Insights:** Gemini integration provides automated economic interpretations of model outputs.
* **CLI Analysis:** Alternative command-line mode using FRED API for US-specific analysis with empirically derived growth rates.
* **Modular Architecture:** Clean separation between data acquisition, mathematical modeling, and UI.

## 💻 Tech Stack
| Layer | Tools |
|-------|-------|
| **Language** | Python 3.x |
| **Web UI** | Streamlit |
| **Data** | Pandas, NumPy, World Bank API (`wbgapi`), FRED API (`fredapi`) |
| **Visualization** | Plotly |
| **AI** | Google Generative AI (Gemini) |
| **Testing** | pytest, pytest-cov |

## 📁 Project Structure
```
solow_growth_app/
├── app.py                        # Entry point for Streamlit (delegates to solow_growth/app.py)
├── main.py                       # Entry point for CLI (delegates to solow_growth/main.py)
├── requirements.txt              # Python dependencies
├── .env                          # API keys (not committed — see setup below)
├── .github/
│   └── copilot-instructions.md
├── solow_growth/                  # Core application package
│   ├── __init__.py
│   ├── app.py                    # Streamlit web UI
│   ├── solow_model.py            # Pure mathematical functions (Solow model calculations)
│   ├── data_fetch.py             # World Bank & FRED API integration
│   └── main.py                   # CLI analysis logic (US data via FRED)
└── tests/
    ├── conftest.py               # Shared fixtures (parameter sets, mock DataFrames)
    ├── test_solow_model.py       # Unit tests for all Solow math functions
    ├── test_data_fetch.py        # Integration tests (API calls mocked)
    ├── test_app.py               # AI insight function tests (Gemini mocked)
    └── test_main.py              # CLI entry point tests
```

## 📐 The Math
The Solow Model steady-state formula:

$$k^* = \left( \frac{s}{n + g + \delta} \right)^{\frac{1}{1-\alpha}}$$

| Parameter | Meaning |
|-----------|---------|
| **s** | Savings rate |
| **n** | Population growth rate |
| **g** | Technological growth rate |
| **δ** | Depreciation rate |
| **α** | Capital share (output elasticity of capital) |

## 🏃 Getting Started
1. Clone the repo.
2. Create a `.env` file with your API keys:
   ```
   FRED_API_KEY=your_fred_key
   GOOGLE_API_KEY=your_google_key
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the web app:
   ```bash
   streamlit run app.py
   ```
5. Or run the CLI analysis:
   ```bash
   python main.py
   ```

## 🧪 Testing
All external API calls (World Bank, FRED, Gemini) are mocked — no API keys required to run tests.

```bash
# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=. --cov-report=term-missing
```

**Test categories:**
| File | Scope | What's tested |
|------|-------|---------------|
| `test_solow_model.py` | Unit | `calculate_steady_state`, `calculate_output_per_worker`, `derive_params` — textbook values, edge cases, monotonicity |
| `test_data_fetch.py` | Integration | `COUNTRY_MAP` validation, FRED fetch, World Bank fetch (year cleaning, column renaming, sorting) |
| `test_app.py` | Integration | `get_ai_insight` — prompt construction, API key configuration, response handling |
| `test_main.py` | Integration | `run_analysis` — correct parameter passing, output verification |

## 🛠️ AI as a Co-pilot
AI (Gemini) was used as a development partner to:
1. **Refactor Code:** Transitioned from static scripts to a modular, functional architecture.
2. **Debug UI State:** Solved reactivity issues between Streamlit sliders and Plotly charts.
3. **Draft Documentation:** Collaborated on technical explanations for complex economic math.

*Note: All economic logic and mathematical implementations were manually verified against macroeconomic theory to ensure accuracy.*