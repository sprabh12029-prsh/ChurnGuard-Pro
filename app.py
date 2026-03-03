import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="ChurnGuard Enterprise", page_icon="📊", layout="wide")

# --- 2. LOAD MODEL ---
@st.cache_resource
def load_model():
    try:
        return joblib.load('churn_model.pkl')
    except:
        return None

model = load_model()

# --- 3. SESSION STATE INITIALIZATION ---
if 'data' not in st.session_state:
    st.session_state['data'] = None

# --- 4. SIDEBAR (THE BURGER MENU) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=60)
    st.title("ChurnGuard AI")
    
    # NAVIGATION MENU
    menu = st.radio(
        "Navigation",
        ["🏠 Home & Upload", "📊 Analytics Dashboard", "⚠️ Risk Assessment", "🧠 Model Performance", "📝 Executive Summary"],
    )
    
    st.markdown("---")
    
    # THRESHOLD SLIDER (The "Sensitivity" Scaler)
    st.header("⚙️ Settings")
    threshold = st.slider("Risk Threshold", 0.0, 1.0, 0.5, 0.05, help="Adjusting this changes who is flagged as 'High Risk'.")
    
    st.markdown("---")
    st.caption(f"Built by: **Prabhmeet Singh Ahuja**")

# --- 5. PAGE: HOME & UPLOAD ---
if menu == "🏠 Home & Upload":
    st.title("👋 Welcome to ChurnGuard AI")
    st.markdown("### Upload your customer data to begin.")
    
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.session_state['data'] = df  # Save to memory
        st.success("✅ File Uploaded Successfully! Navigate to 'Analytics' or 'Risk' to see results.")
        st.dataframe(df.head(), use_container_width=True)
    
    elif st.session_state['data'] is not None:
        st.info("Using previously uploaded data.")
        st.dataframe(st.session_state['data'].head(), use_container_width=True)
    else:
        st.warning("Waiting for file upload...")

# --- 6. PAGE: ANALYTICS DASHBOARD ---
elif menu == "📊 Analytics Dashboard":
    st.title("📊 Customer Analytics")
    
    if st.session_state['data'] is None:
        st.error("Please upload data on the Home page first.")
    else:
        df = st.session_state['data']
        
        # KEY METRICS ROW
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Customers", len(df))
        c2.metric("Avg Monthly Bill", f"${df['monthly_bill'].mean():.2f}")
        c3.metric("Avg Support Tickets", f"{df['support_tickets'].mean():.1f}")
        
        st.markdown("---")
        
        # GRAPHS ROW 1
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Distribution of Monthly Bills")
            fig_bill = px.histogram(df, x="monthly_bill", nbins=20, title="Bill Distribution", color_discrete_sequence=['#636EFA'])
            st.plotly_chart(fig_bill, use_container_width=True)
            
        with col2:
            st.subheader("Support Tickets Frequency")
            fig_tickets = px.bar(df['support_tickets'].value_counts().reset_index(), x='support_tickets', y='count', title="Tickets per Customer", color_discrete_sequence=['#EF553B'])
            st.plotly_chart(fig_tickets, use_container_width=True)

# --- 7. PAGE: RISK ASSESSMENT ---
elif menu == "⚠️ Risk Assessment":
    st.title("⚠️ Churn Risk Analysis")
    
    if st.session_state['data'] is None:
        st.error("Please upload data first.")
    else:
        df = st.session_state['data'].copy()
        
        # PREDICTION ENGINE
        required_cols = ['age', 'monthly_bill', 'support_tickets']
        if all(col in df.columns for col in required_cols):
            
            # Predict
            probs = model.predict_proba(df[required_cols])[:, 1]
            df['Risk Score'] = probs
            # USE THE SLIDER THRESHOLD HERE
            df['Prediction'] = np.where(probs > threshold, "🔴 CHURN", "🟢 SAFE")
            
            # 1. PROBABILITY DISTRIBUTION GRAPH
            st.subheader("📈 Probability of Churn Distribution")
            st.caption("This graph shows how confident the model is. Peaks on the right mean high risk.")
            fig_dist = px.histogram(df, x="Risk Score", nbins=20, color="Prediction", 
                                  color_discrete_map={"🔴 CHURN": "red", "🟢 SAFE": "green"})
            st.plotly_chart(fig_dist, use_container_width=True)
            
            # 2. DONUT CHART
            col1, col2 = st.columns([1, 2])
            with col1:
                st.subheader("Churn Ratio")
                counts = df['Prediction'].value_counts()
                fig_pie = px.pie(values=counts, names=counts.index, hole=0.5, 
                               color_discrete_map={"🔴 CHURN": "red", "🟢 SAFE": "green"})
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col2:
                st.subheader("🚨 High Risk Alert List")
                # Filter by threshold
                high_risk = df[df['Risk Score'] > threshold].sort_values(by="Risk Score", ascending=False)
                st.dataframe(high_risk.style.applymap(lambda x: 'background-color: #ffcccc', subset=['Risk Score']), height=300, use_container_width=True)
                
        else:
            st.error(f"Missing columns: {required_cols}")

# --- 8. PAGE: MODEL PERFORMANCE ---
elif menu == "🧠 Model Performance":
    st.title("🧠 AI Brain Metrics")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Model Accuracy: **85.0%**")
        st.progress(85)
        st.caption("Based on validation testing dataset.")
    
    with col2:
        st.markdown("### Recall (Sensitivity): **92.0%**")
        st.progress(92)
        st.caption("Ability to catch true churners.")

    st.markdown("---")
    st.subheader("🔍 Feature Importance Matrix")
    st.caption("What drives the decision making?")
    
    # Hardcoded for display based on your previous training results
    importance_data = pd.DataFrame({
        'Feature': ['Support Tickets', 'Monthly Bill', 'Age'],
        'Importance': [0.55, 0.35, 0.10]
    })
    fig_imp = px.bar(importance_data, x='Importance', y='Feature', orientation='h', color='Importance', color_continuous_scale='Viridis')
    st.plotly_chart(fig_imp, use_container_width=True)

# --- 9. PAGE: SUMMARY ---
elif menu == "📝 Executive Summary":
    st.title("📝 Executive Summary")
    
    if st.session_state['data'] is not None:
        df = st.session_state['data']
        # Recalculate predictions just for summary
        probs = model.predict_proba(df[['age', 'monthly_bill', 'support_tickets']])[:, 1]
        churn_count = len(df[probs > threshold])
        total = len(df)
        revenue_risk = churn_count * df['monthly_bill'].mean()
        
        st.success(f"### 🚩 System Flagged {churn_count} At-Risk Customers")
        
        col1, col2 = st.columns(2)
        col1.info(f"**Potential Revenue Loss:** ${revenue_risk:,.2f}")
        col2.info(f"**Action Required:** Immediate outreach to {churn_count} users.")
        
        st.markdown("### 📢 Recommended Actions")
        st.markdown(f"""
        1. **High Priority:** The {churn_count} customers identified in the **Risk Assessment** tab should be contacted immediately.
        2. **Strategy:** Customers with high 'Support Tickets' should be routed to a Senior Manager.
        3. **Offer:** Consider a 15% discount for customers with Bill > $100.
        """)
        
        # Download Button
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Final Report", csv, "final_report.csv", "text/csv")
        
    else:
        st.info("Upload data to generate the executive summary.")