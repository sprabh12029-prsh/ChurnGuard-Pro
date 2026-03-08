import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import roc_curve
from xgboost import XGBClassifier
import shap
from fpdf import FPDF, XPos, YPos
import uvicorn

app = FastAPI(title="ChurnGuard Pro - Indigo Analytics API", version="1.0.0")

# Enhanced CORS for global deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

class TrainRequest(BaseModel):
    target_col: str
    model_choice: str

class PredictRequest(BaseModel):
    avg_ticket_price: float
    booking_abandonment_rate: float
    rewards_points: float

def get_indigo_data():
    # Changed the filename to force a fresh data generation!
    file_path = "indigo_full_dataset_v2.csv" 
    
    if not os.path.exists(file_path):
        np.random.seed(6)
        size = 1240
        data = {
            'pnr_id': [f"6E{i}" for i in range(1000, 1000 + size)],
            'route': np.random.choice(['DEL-BOM', 'BOM-BLR', 'DEL-DXB', 'MAA-SIN'], size),
            'fare_class': np.random.choice(['Economy', 'Corporate', 'Business'], size),
            'miles_flown_yearly': np.random.normal(5000, 2000, size),
            'booking_abandonment_rate': np.random.uniform(0, 0.7, size),
            '6E_rewards_points': np.random.poisson(2500, size),
            'is_churned': np.random.choice([0, 1], size, p=[0.75, 0.25])
        }
        pd.DataFrame(data).to_csv(file_path, index=False)
    return pd.read_csv(file_path)

# Health Check Endpoints
@app.get("/api/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "healthy", "service": "ChurnGuard Pro API", "version": "1.0.0"}

@app.get("/api/status")
async def status():
    """Detailed status endpoint"""
    try:
        df = get_indigo_data()
        return {
            "status": "operational",
            "dataset_loaded": True,
            "total_records": len(df),
            "service": "ChurnGuard Pro - Indigo Airlines Intelligence Platform"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/api/train")
async def train_model(request: TrainRequest):
    df = get_indigo_data()

    # Safely drop pnr_id to prevent KeyErrors
    if 'pnr_id' in df.columns:
        df = df.drop(columns=['pnr_id'])

    le = LabelEncoder()
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = le.fit_transform(df[col].astype(str))

    X = df.drop(columns=[request.target_col])
    y = df[request.target_col]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # XGBoost Training
    model = XGBClassifier(eval_metric='logloss')
    model.fit(X_train, y_train)

    # 1. SHAP Signals
    explainer = shap.Explainer(model)
    shap_values = explainer(X_test)
    importance = [{"feature": col, "importance": float(val)}
                  for col, val in zip(X.columns, np.abs(shap_values.values).mean(0))]
    
    # 2. ROC Curve Reliability
    y_prob = model.predict_proba(X_test)[:, 1]
    fpr, tpr, _ = roc_curve(y_test, y_prob)
    roc_data = [{"fpr": round(f, 3), "tpr": round(t, 3)} for f, t in zip(fpr[::5], tpr[::5])]
    
    # 3. Fleet Route Risk
    raw_df = get_indigo_data()
    route_stats = raw_df.groupby('route')['is_churned'].mean().reset_index()
    fleet_data = [{"route": r, "risk": round(s*100, 1)} for r, s in zip(route_stats['route'], route_stats['is_churned'])]
    
    return {
        "dashboard": {"active_passengers": len(df), "churn_rate": float(y.mean()*100)},
        "feature_importance": sorted(importance, key=lambda x: x['importance'], reverse=True),
        "roc_data": roc_data,
        "fleet_data": fleet_data
    }

@app.post("/api/predict")
async def predict_single(request: PredictRequest):
    risk = (request.booking_abandonment_rate * 0.7) + (0.3 if request.rewards_points < 1000 else 0)
    risk_pct = min(risk * 100, 100)
    voucher = "N/A"
    if risk_pct > 75: 
        voucher = "₹2,500 + Priority Boarding"
    elif risk_pct > 40: 
        voucher = "₹1,000 Next-Flight Credit"
    return {"churn_probability": risk_pct, "voucher": voucher}

@app.get("/api/download-report")
async def generate_report():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", 'B', 16)
    pdf.cell(200, 10, "Indigo 6E Intelligence Executive Report", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    pdf.set_font("helvetica", '', 12)
    pdf.ln(10)
    pdf.cell(200, 10, "Analyst: Prabhmeet Singh Ahuja", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    report_file = "Indigo_6E_Report.pdf"
    pdf.output(report_file)
    return FileResponse(report_file, filename="Indigo_6E_Executive_Report.pdf") 

if __name__ == "__main__":
    # Get host and port from environment variables or use defaults
    host = os.getenv("API_HOST", "0.0.0.0")  # 0.0.0.0 for external access
    port = int(os.getenv("API_PORT", 8000))
    
    print(f"\n🚀 ChurnGuard Pro - Indigo Analytics API")
    print(f"📍 Starting on {host}:{port}")
    print(f"🌐 API will be accessible at http://localhost:{port}")
    print(f"📊 Health Check: http://localhost:{port}/api/health")
    print(f"📋 API Docs: http://localhost:{port}/docs\n")
    
    uvicorn.run(app, host=host, port=port)
