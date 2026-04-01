# Solow Growth Lab - Project Guidelines

## Purpose
Educational economics application demonstrating the Solow Growth Model with real-world data integration and AI-powered analysis. Mathematical accuracy and pedagogical clarity are primary objectives.

## Architecture
**Modular Design** - Strict separation of concerns inside the `solow_growth/` package:
- `solow_growth/data_fetch.py`: World Bank API (multi-country GDP) and FRED API (US GDP) integration
- `solow_growth/solow_model.py`: Pure mathematical functions (Solow model calculations)
- `solow_growth/app.py`: Streamlit UI logic
- `solow_growth/main.py`: CLI analysis alternative (US-only, FRED-based)
- `app.py` / `main.py` (root): Thin entry points that delegate to `solow_growth/`
- `tests/`: pytest test suite with mocked external APIs

**Key Principle**: Economic logic and mathematical implementations must be manually verifiable against macroeconomic theory.

## Build and Test
```bash
# Setup (one time)
pip install -r requirements.txt

# Create .env with required keys:
# FRED_API_KEY=your_fred_key
# GOOGLE_API_KEY=your_google_key

# Run the app
streamlit run app.py

# Run all tests (no API keys needed — all external calls are mocked)
pytest tests/ -v

# Run tests with coverage
pytest tests/ --cov=. --cov-report=term-missing

# Test individual modules
python -m solow_growth.solow_model
python -m solow_growth.main
```

## Code Style
- **Functions**: Pure functions for calculations (see `solow_growth/solow_model.py`)
- **Docstrings**: Required for all economic functions with parameter explanations
- **Mathematical Notation**: Use Greek letters in comments matching LaTeX (α, δ, etc.)
- **Type Hints**: Not currently used, but welcome for clarity

## Conventions
- **Parameter Naming**: Follow economic standards (s=savings, n=population growth, g=tech growth, δ=depreciation, α=capital share)
- **Steady State Variables**: Suffix with `_star` (e.g., `k_star`, `y_star`)
- **Data Sources**: Always cite when using external economic data or formulas
- **AI Integration**: Use Gemini for insights, but verify economic accuracy manually
- **Component Scaling**: When comparing theoretical ratios to real dollar values, document scaling factors clearly (see `solow_growth/app.py`)

## Testing Conventions
- **Framework**: pytest with pytest-cov
- **Test location**: All tests in `tests/` directory
- **Shared fixtures**: Use `tests/conftest.py` for reusable parameter sets and mock DataFrames
- **Naming**: `test_<function_name>_<scenario>` (e.g., `test_textbook_values`, `test_higher_savings_increases_k_star`)
- **External APIs**: Always mock FRED, World Bank, and Gemini calls — no test should require real API keys
- **Mathematical verification**: Test Solow functions against hand-calculable expected values with explicit comments showing the calculation
- **New functions**: Every new function must have at least one corresponding test
- **Test categories**:
  - `test_solow_model.py`: Pure math unit tests (textbook values, edge cases, monotonicity)
  - `test_data_fetch.py`: Data layer integration tests (mocked APIs, data transformation validation)
  - `test_app.py`: AI insight function tests (prompt construction, response handling)
  - `test_main.py`: CLI entry point tests (parameter flow, output verification)

## Documentation Sync Rules
When making changes to the project, keep all documentation in sync:
- **Adding/modifying a function** → add or update its corresponding test in `tests/`
- **Changing module responsibilities** → update Architecture section in both README.md and this file
- **Adding dependencies** → update `requirements.txt` AND Tech Stack table in README.md
- **Changing API integrations** → update data source references in README.md
- **Modifying Solow formula** → update Economic Domain Knowledge section below
- **Adding test files** → update Project Structure in README.md and test categories above

## Economic Domain Knowledge
The Solow Model steady-state formula is:
```
k* = (s / (n + g + δ))^(1/(1-α))
```
Any modifications to this core equation require explicit justification and source citation.
