# 📈 Interactive Solow Growth Lab
**An AI-Co-piloted Economic Analysis Tool**

## 🎯 Overview
This project is an interactive web application that bridges **Neoclassical Growth Theory** with **Real-World Data**. It allows users to manipulate Solow Growth Model parameters and see how theoretical "Steady States" compare against historical US GDP data fetched via the FRED API.

## 🚀 Key Features
* **Live Data Integration:** Pulls real-time Real GDP per Capita from the St. Louis Fed (FRED).
* **Interactive Modeling:** Dynamic Plotly visualizations that respond to parameter shifts (Savings, Population, Depreciation).
* **AI-Powered Insights:** Integrated with Gemini 1.5 to provide automated economic interpretations of model outputs.
* **Modular Architecture:** Clean separation between data acquisition, mathematical modeling, and UI.

## 💻 Tech Stack
* **Language:** Python 3.x
* **Framework:** Streamlit (Frontend/Web)
* **Data:** Pandas (Analysis), FRED API (Source)
* **Visuals:** Plotly (Interactivity)
* **AI:** Google Generative AI (LLM Integration)

## 🛠️ AI as a Co-pilot
In this project, I utilized AI (Gemini) as a development partner to:
1. **Refactor Code:** Transitioned from static scripts to a modular, functional architecture.
2. **Debug UI State:** Solved reactivity issues between Streamlit sliders and Plotly charts.
3. **Draft Documentation:** Collaborated on technical explanations for complex economic math.
*Note: All economic logic and mathematical implementations were manually verified against macroeconomic theory to ensure accuracy.*

## 🏃 How to Run
1. Clone the repo.
2. Create a `.env` with your `FRED_API_KEY` and `GOOGLE_API_KEY`.
3. Run `pip install -r requirements.txt`.
4. Run `streamlit run app.py`.