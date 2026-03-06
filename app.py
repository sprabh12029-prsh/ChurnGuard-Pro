import streamlit as st
import pandas as pd
import numpy as np
import xgboost as xgb
import tensorflow as tf
import shap
import matplotlib.pyplot as plt
import seaborn as sns
import time
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.metrics import confusion_matrix, mean_absolute_error, r2_score
from sklearn.preprocessing import LabelEncoder

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="ChurnGuard-Pro AI", page_icon="🚀", layout="wide")

# --- 2. START-UP ANIMATION ---
# We use session_state so the animation only plays once per visit, not every time you click a button.
if 'app_loaded' not in st.session_state:
    splash = st.empty()
    with splash.container():
        st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; font-size: 5em;'>🚀 ChurnGuard-Pro</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: gray;'>Built by Prabhmeet Singh Ahuja</h3>", unsafe_allow_html=True)
        
        progress_text = "Initializing AI Engine..."
        my_bar = st.progress(0, text=progress_text)
        
        for percent_complete in range(100):
            time.sleep(0.01)
            my_bar.progress(percent_complete + 1, text=progress_text)
            
        time.sleep(0.5)
        st.balloons()
    
    splash.empty() # Clears the animation off the screen
    st.session_state['app_loaded'] = True

# --- 3. DATA FRAMEWORK ---
@st.cache_data
def load_data():
    return pd.read_csv('customer_churn_data.csv')

try:
    df = load_data()
except FileNotFoundError:
    st.error("🚨 Dataset not found! Please ensure 'customer_churn_data.csv' is in the same folder.")
    st.stop()

# --- 4. NAVIGATION MENU (SIDEBAR) ---
st.sidebar.title("🧭 Main Menu")
menu_selection = st.sidebar.radio(
    "Go to:",
    ["📊 Dashboard Overview", "🧠 AI AutoML Engine", "⚙️ Options & Export"]
)

st.sidebar.markdown("---")
st.sidebar.info("Deployed on AWS EC2: 13.48.71.21")

# ==========================================
# PAGE 1: DASHBOARD OVERVIEW
# ==========================================
if menu_selection == "📊 Dashboard Overview":
    st.title("📊 System Dashboard")
    st.markdown("Welcome to the **ChurnGuard-Pro** administrative overview.")
    
    # Top Level Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Records", len(df))
    col2.metric("Total Features", len(df.columns) - 1)
    col3.metric("System Status", "Online - AWS Stockholm")
    
    st.markdown("### 📋 Dataset Preview")
    st.dataframe(df.head(10), use_container_width=True)
    
    st.markdown("### 📈 Quick Statistics")
    st.write(df.describe())

# ==========================================
# PAGE 2: AI AUTO-ML ENGINE (The Dynamic Fix)
# ==========================================
elif menu_selection == "🧠 AI AutoML Engine":
    st.title("🧠 Dynamic AI Pipeline")
    
    col1, col2 = st.columns([1, 3])
    with col1:
        target_col = st.selectbox(
            "🎯 Select Target Column:", 
            options=df.columns.tolist(),
            index=len(df.columns)-1
        )
    
    y = df[target_col]
    X = df.drop(target_col, axis=1)

    # Clean up features
    cols_to_drop = [col for col in X.columns if X[col].nunique() == len(X)]
    X = X.drop(columns=cols_to_drop)
    X = pd.get_dummies(X, drop_first=True) 

    # Smart Detection Logic
    is_classification = True
    if pd.api.types.is_numeric_dtype(y) and y.nunique() > 10:
        is_classification = False

    if is_classification and y.dtype == 'object':
        y = LabelEncoder().fit_transform(y)

    # Train/Test Split
    if is_classification:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
        st.markdown(f"**Task Detected:** 🟢 Classification (`{target_col}`)")
        model_options = ["XGBoost Classifier", "Logistic Regression", "Deep Learning (Classification)"]
    else:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        st.markdown(f"**Task Detected:** 🔵 Regression (`{target_col}`)")
        model_options = ["XGBoost Regressor", "Linear Regression", "Deep Learning (Regression)"]

    model_choice = st.radio("Select Model Architecture", model_options, horizontal=True)
    
    # Training Button Controller
    if st.button("🚀 Run AI Analysis", type="primary", use_container_width=True):
        with st.spinner(f"Training {model_choice}..."):
            
            # --- MODEL ROUTING ---
            if "XGBoost Classifier" in model_choice:
                model = xgb.XGBClassifier(eval_metric='logloss')
                model.fit(X_train, y_train)
                preds = model.predict(X_test)
            elif "XGBoost Regressor" in model_choice:
                model = xgb.XGBRegressor()
                model.fit(X_train, y_train)
                preds = model.predict(X_test)
            elif "Logistic Regression" in model_choice:
                model = LogisticRegression(max_iter=2000)
                model.fit(X_train, y_train)
                preds = model.predict(X_test)
            elif "Linear Regression" in model_choice:
                model = LinearRegression()
                model.fit(X_train, y_train)
                preds = model.predict(X_test)
            elif "Deep Learning (Classification)" in model_choice:
                model = tf.keras.models.Sequential([
                    tf.keras.layers.Dense(32, activation='relu', input_shape=(X_train.shape[1],)),
                    tf.keras.layers.Dense(1, activation='sigmoid')
                ])
                model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
                model.fit(X_train, y_train, epochs=15, verbose=0)
                preds = (model.predict(X_test).flatten() > 0.5).astype(int)
            elif "Deep Learning (Regression)" in model_choice:
                model = tf.keras.models.Sequential([
                    tf.keras.layers.Dense(32, activation='relu', input_shape=(X_train.shape[1],)),
                    tf.keras.layers.Dense(1, activation='linear')
                ])
                model.compile(optimizer='adam', loss='mse')
                model.fit(X_train, y_train, epochs=15, verbose=0)
                preds = model.predict(X_test).flatten()

            # --- EVALUATION ---
            st.markdown("---")
            c1, c2 = st.columns(2)

            with c1:
                if is_classification:
                    st.subheader("📉 Confusion Matrix")
                    cm = confusion_matrix(y_test, preds)
                    fig_cm, ax_cm = plt.subplots()
                    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax_cm)
                    ax_cm.set_xlabel('Predicted')
                    ax_cm.set_ylabel('Actual')
                    st.pyplot(fig_cm)
                else:
                    st.subheader("📈 Actual vs Predicted")
                    fig_reg, ax_reg = plt.subplots()
                    ax_reg.scatter(y_test, preds, alpha=0.5, color='royalblue')
                    ax_reg.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
                    st.pyplot(fig_reg)
                    st.success(f"Mean Absolute Error (MAE): {mean_absolute_error(y_test, preds):.2f}")

            with c2:
                st.subheader("🔍 Interpretability (SHAP)")
                if "XGBoost" in model_choice:
                    explainer = shap.TreeExplainer(model)
                    shap_values = explainer.shap_values(X_test)
                    fig_shap, ax_shap = plt.subplots()
                    shap.summary_plot(shap_values, X_test, show=False)
                    st.pyplot(fig_shap)
                else:
                    st.info("SHAP Global Summary is currently optimized for Tree-based models like XGBoost.")

# ==========================================
# PAGE 3: OPTIONS & EXPORT
# ==========================================
elif menu_selection == "⚙️ Options & Export":
    st.title("⚙️ System Options")
    st.markdown("Manage application data and download reports.")
    
    st.subheader("💾 Data Export")
    csv_file = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Raw Dataset (CSV)", data=csv_file, file_name='customer_churn_data.csv', mime='text/csv')
    
    st.subheader("🧹 Maintenance")
    if st.button("Clear Application Cache", type="secondary"):
        st.cache_data.clear()
        st.success("Cache cleared successfully! Data will reload on next run.")
        
    st.markdown("---")
    st.caption("ChurnGuard-Pro v2.0 | Hosted on AWS EC2 Ubuntu 24.04")