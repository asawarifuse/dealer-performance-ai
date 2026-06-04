# Dealer Performance Intelligence System

AI-powered dealer performance monitoring system with Gen AI conversational analytics. Built for automobile dealership networks.

## Overview
Monitors 500 dealers across 11 KPIs over 24 months (12,000-row dataset). Detects underperformance, explains causes using XAI, and recommends interventions via counterfactual AI. Includes a Gen AI Dashboard Speaker for natural language queries.

## Features
- 500 dealers × 24 months × 11 KPIs synthetic dataset
- Weighted composite scoring engine
- Anomaly detection (Isolation Forest)
- XAI explainability (SHAP)
- Counterfactual intervention recommendations (DiCE)
- 5-page Power BI dashboard
- Gen AI Dashboard Speaker (Google Gemini)
- Deployed on Streamlit Cloud

## Tech Stack
Python | Pandas | NumPy | Scikit-learn | XGBoost | SHAP | DiCE | Power BI | Streamlit | Plotly | Google Gemini

## Dashboard Pages
1. **Executive Summary** — High-level KPIs, sales trends, bottom 10 dealers
2. **Dealer Deep Dive** — Single dealer view, 11 KPI trends
3. **Dealer Comparison** — Regional filter, scatter plot, ranking table
4. **Anomaly Center** — Flagged dealers, anomaly trends by month & region
5. **AI Assistant** — Natural language Q&A with Dashboard Speaker

## Screenshots

### Page 1: Executive Summary
![Executive Summary](04_PowerBI/screenshots/page1_executive_summary.png)

### Page 2: Dealer Deep Dive
![Dealer Deep Dive](04_PowerBI/screenshots/page2_dealer_deep_dive.png)

### Page 3: Dealer Comparison
![Dealer Comparison](04_PowerBI/screenshots/page3_dealer_comparison.png)

### Page 4: Anomaly Center
![Anomaly Center](04_PowerBI/screenshots/page4_anomaly_center.png)

### Page 5: AI Assistant
![AI Assistant](04_PowerBI/screenshots/page5_ai_assistant.png)

### SHAP Explainability
![SHAP Summary](04_PowerBI/screenshots/shap_summary.png)

## Live Demo
[View App](https://dealer-performance-ai-wppcvadb4ixigqwv6fkcoz.streamlit.app/)

## Folder Structure
├── 01_Raw_Data/ # Original CSVs
├── 02_Excel_Outputs/ # Scored datasets, counterfactuals
├── 03_Python_Scripts/ # Data generation, ML, XAI, counterfactuals
├── 04_PowerBI/ # Dashboard .pbix + screenshots
├── 05_Streamlit_App/ # App files
├── 06_Documentation/ # Data dictionary, methodology
└── README.md

## How to Run Locally
1. Clone repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run app: `streamlit run app.py`

## Author
Asawari Vasantrao Fuse
2nd Year, CSE (Data Science)
