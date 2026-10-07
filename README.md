# agritech-iot-dashboard
Time-series analytics and predictive machine learning dashboard for agricultural IoT sensor telemetry.
# 🌾 AgriTech IoT Sensor Analytics Dashboard

An end-to-end Data Science and IoT telemetry processing application built in Python. This tool ingests microclimate and soil sensor telemetry across multiple crop zones, applies time-series feature engineering, and predicts soil moisture depletion to optimize precision irrigation.

![Status](https://img.shields.io/badge/Status-In_Development-orange)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Stack](https://img.shields.io/badge/Stack-Pandas_%7C_Scikit--Learn_%7C_Streamlit-green)

---

## 📌 Features & Key Objectives
- **Data Engineering Pipeline:** Ingestion, cleaning, and rolling-window aggregations of high-frequency IoT sensor streams using **Pandas**.
- **Predictive Analytics:** Forecasting 24-hour soil moisture trends using **Scikit-Learn** regression models to prevent crop water stress.
- **Interactive Dashboard:** Dynamic telemetry visualizations (temperature, humidity, soil moisture) and field alert systems built with **Streamlit** and **Plotly**.

---

## 🛠️ Tech Stack & Tools
- **Language:** Python
- **Data Manipulation:** Pandas, NumPy
- **Machine Learning:** Scikit-Learn
- **Visualization & UI:** Plotly, Streamlit
- **Environment & Version Control:** VS Code, Git, GitHub

---

## 📊 Dataset Overview
This project processes time-series telemetry representing key environmental metrics:
- **Soil Moisture (%)**
- **Ambient Temperature (°C)**
- **Air Humidity (%)**
- **Sensor Timestamps & Crop Zone IDs**

---

## 🚀 Future Roadmap
- [ ] Complete Exploratory Data Analysis (EDA) on raw sensor logs.
- [ ] Build automated feature pipeline (rolling hourly averages, lag features).
- [ ] Train and evaluate Scikit-Learn regression algorithms (Linear Regression vs. Random Forest).
- [ ] Deploy Streamlit web application to Streamlit Community Cloud.

---
*Developed by Daniel Thompson — BSc Computer Science Student, University of Liverpool.*
