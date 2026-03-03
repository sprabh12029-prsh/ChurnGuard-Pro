# 🔮 ChurnGuard AI - Enterprise Customer Retention System

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-Machine%20Learning-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Status](https://img.shields.io/badge/Status-Production%20Ready-success?style=for-the-badge)

## 📖 Project Overview
**ChurnGuard AI** is a full-stack Machine Learning application designed to help businesses predict which customers are likely to cancel their subscriptions ("churn"). 

Instead of a simple script, this is a **deployed product** that allows non-technical stakeholders (Sales Managers, Executives) to upload customer data, visualize risks, and generate automated PowerPoint reports for board meetings.

---

## 🛠️ The Tech Stack: What We Used & Why

This project was built using industry-standard Data Science tools. Here is the breakdown of every technology decision:

### 1. The Core Application
* **🐍 Python 3.12**
    * **What it is:** The primary programming language for Data Science.
    * **Why we used it:** Python offers the strongest ecosystem of libraries for data manipulation and AI, making it the industry standard for building scalable ML pipelines.

* **⚡ Streamlit**
    * **What it is:** An open-source Python framework for building custom web apps.
    * **Why we used it:** It allows us to turn data scripts into shareable web applications in minutes, not weeks. It handles the frontend UI (buttons, sliders, file uploaders) entirely in Python, removing the need for HTML/CSS/JavaScript.

### 2. Machine Learning Engine
* **🤖 Scikit-Learn (Random Forest Classifier)**
    * **What it is:** The robust library for classical machine learning algorithms.
    * **Why we used it:** We chose the **Random Forest** algorithm because:
        1.  It handles non-linear relationships better than Logistic Regression.
        2.  It is an "Ensemble" method (combining many decision trees), making it resistant to overfitting.
        3.  It provides **Feature Importance**, allowing us to explain *why* a customer is churning (e.g., High Bill vs. Low Tenure).

* **⚖️ SMOTE (Synthetic Minority Over-sampling Technique)**
    * **What it is:** A technique to handle imbalanced datasets.
    * **Why we used it:** Real-world churn is rare (e.g., only 10% of users leave). A standard model might ignore them to get "high accuracy." SMOTE generates synthetic examples of churners to force the model to learn their patterns effectively.

### 3. Data Processing
* **🐼 Pandas**
    * **What it is:** A fast, powerful, flexible, and easy-to-use open-source data analysis and manipulation tool.
    * **Why we used it:** To ingest raw CSV files, clean data (handling missing values), and engineer new features like `Bill_Per_Support_Ticket`. It acts as the SQL-like engine of our Python script.

* **🔢 NumPy**
    * **What it is:** The fundamental package for scientific computing with Python.
    * **Why we used it:** Used for high-performance mathematical operations, creating synthetic data for testing, and handling arrays that feed into the Machine Learning model.

### 4. Visualization & Reporting
* **📊 Plotly Express**
    * **What it is:** An interactive graphing library.
    * **Why we used it:** Unlike static images (Matplotlib), Plotly charts are interactive. Users can hover over bars to see exact numbers, zoom in on data clusters, and filter results dynamically. This creates a superior User Experience (UX).

* **📽️ Python-PPTX**
    * **What it is:** A library for creating and updating PowerPoint (.pptx) files.
    * **Why we used it:** Business executives often prefer slide decks over dashboards. This library automates the manual work of reporting by generating a "Board-Ready" presentation with the click of a button, filled with the latest live data.

### 5. Operations (MLOps)
* **💾 Joblib**
    * **What it is:** A set of tools to provide lightweight pipelining in Python.
    * **Why we used it:** To "serialize" (save) the trained machine learning model (`churn_model.pkl`). This means we don't have to retrain the model every time a user visits the website. The app simply loads the "brain" instantly, ensuring zero latency.

---

## 🚀 Key Features

1.  **🔍 Predictive Analytics Engine:** instantly flags customers with a 0-100% risk score.
2.  **🎚️ Dynamic Thresholding:** A slider that allows managers to adjust the sensitivity of the model (e.g., "Show me everyone with >50% risk" vs ">80% risk").
3.  **📉 Interactive Dashboards:** Visual histograms showing the distribution of monthly bills and support tickets.
4.  **📑 Automated Executive Reporting:** Generates a downloadable PowerPoint presentation with executive summaries and strategic recommendations.
5.  **🔐 Role-Based Session State:** Simulates a secure login environment (Data Scientist vs Manager views).

---

## 📂 Project Structure

```text
ChurnGuard-Pro/
├── app.py                  # The Main Streamlit Application (Frontend & Logic)
├── pro_model.py            # The Model Training Pipeline (Backend)
├── churn_model.pkl         # The Saved AI "Brain" (Binary File)
├── customer_churn_data.csv # Synthetic Data for Testing
├── requirements.txt        # List of dependencies for Cloud Deployment
└── README.md               # Project Documentation
---

## 🌟 Why This Project Matters

**ChurnGuard AI** is more than just code—it addresses a critical multi-billion dollar business challenge. In the corporate world, acquiring a new customer costs **5 to 25 times more** than retaining an existing one. This tool bridges the gap between raw data and actionable profitability.

### 1. 💼 Business Impact
* **💰 Revenue Protection:** Acts as an "Early Warning System" to flag high-risk customers *before* they leave, allowing companies to save potentially millions in lost revenue.
* **🎯 Targeted Efficiency:** Instead of spamming all users, the **Risk Threshold Slider** allows marketing teams to focus their budget only on the top 10% most critical cases.
* **🧠 Root Cause Analysis:** The **Feature Importance Matrix** moves beyond simple prediction to explain *why* churn is happening (e.g., distinguishing between price sensitivity vs. poor support experiences).

### 2. 👥 Real-World Utility
This project simulates a professional Enterprise Data Science workflow, serving multiple stakeholders:
* **For Sales Managers:** A prioritized **"Hit List"** of at-risk customers is generated instantly for retention campaigns.
* **For Executives (C-Suite):** The **Automated PowerPoint Generator** converts complex analytics into Board-Ready slides in seconds, eliminating manual reporting hours.
* **For Data Scientists:** The **Notebook Workflow** tab ensures model transparency, allowing technical teams to audit accuracy, recall, and data integrity.

### 3. 🎓 Skills Demonstrated
This repository demonstrates **Full-Stack Data Science** capabilities:
* **End-to-End Ownership:** From raw data engineering to cloud deployment.
* **Business Acumen:** integrating ROI calculations and financial risk assessments directly into the code.
* **UX/UI Design:** Creating a secure, role-based environment with an intuitive interface.
* **Automation:** Using Python to automate manual administrative tasks (Report Generation).