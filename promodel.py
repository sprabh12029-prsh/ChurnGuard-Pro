import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report, roc_auc_score
from imblearn.over_sampling import SMOTE # Fixes the "rare churn" problem

# --- 1. DATA GENERATION (SIMULATED ENTERPRISE DATA) ---
# We are adding "Tenure" (how long they've been a customer) to make it realistic.
np.random.seed(42)
n = 5000 # More data
data = pd.DataFrame({
    'age': np.random.randint(18, 70, size=n),
    'monthly_bill': np.random.normal(65, 30, size=n).clip(20, 200), # Normal distribution
    'support_tickets': np.random.poisson(2, size=n), # Poisson distribution for counts
    'tenure_months': np.random.randint(1, 72, size=n) # 1 month to 6 years
})

# Complex Churn Logic (Non-linear relationships)
# Rule: High tickets + High Bill = Churn
# Rule: Low Tenure + High Bill = Churn
base_prob = 0.05
risk_score = (data['support_tickets'] * 0.15) + (data['monthly_bill'] / 200) - (data['tenure_months'] * 0.01)
churn_prob = 1 / (1 + np.exp(-(risk_score - 2))) # Sigmoid function (Professional probability curve)
data['is_churned'] = np.random.binomial(1, churn_prob)

print(f"--- Data Generated: {n} Rows ---")
print(f"Churn Rate: {data['is_churned'].mean():.2%}")

# --- 2. FEATURE ENGINEERING (The "Secret Sauce") ---
# Senior DS create new clues from existing ones.
print("\n--- Engineering Features ---")
data['bill_per_ticket'] = data['monthly_bill'] / (data['support_tickets'] + 1) # Avoid divide by zero
data['is_new_customer'] = (data['tenure_months'] < 6).astype(int)
data['high_maintenance'] = (data['support_tickets'] > 3).astype(int)

X = data.drop('is_churned', axis=1)
y = data['is_churned']

# --- 3. SMOTE (Handling Imbalance) ---
# In real life, churners are rare. SMOTE creates "fake" churners to train the model better.
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X, y)
print(f"Data after SMOTE resampling: {len(X_resampled)} rows")

# --- 4. XGBOOST with HYPERPARAMETER TUNING ---
# We don't guess parameters. We use GridSearch to scientifically find the best ones.
print("\n--- Tuning XGBoost (This may take a minute) ---")
X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=42)

# The "Grid" of options to try
param_grid = {
    'max_depth': [3, 5],
    'learning_rate': [0.01, 0.1],
    'n_estimators': [100, 200],
    'subsample': [0.8]
}

xgb_model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss')
grid_search = GridSearchCV(estimator=xgb_model, param_grid=param_grid, cv=3, scoring='roc_auc', verbose=1)
grid_search.fit(X_train, y_train)

best_model = grid_search.best_estimator_
print(f"Best Parameters Found: {grid_search.best_params_}")

# --- 5. BUSINESS EVALUATION (ROI) ---
# A Senior DS calculates MONEY saved, not just accuracy.
y_pred = best_model.predict(X_test)
y_prob = best_model.predict_proba(X_test)[:, 1]

print("\n--- Professional Evaluation ---")
print(f"ROC-AUC Score: {roc_auc_score(y_test, y_prob):.4f} (Industry Standard Metric)")

# ROI Calculator
# Assumptions:
# - Avg Customer Value (LTV): $1000
# - Cost to intervene (Discount/Call): $50
# - Success rate of intervention: 30%

# We only target people with > 75% churn probability
high_risk_customers = X_test[y_prob > 0.75]
n_targeted = len(high_risk_customers)
true_churners_caught = y_test.loc[high_risk_customers.index].sum()

cost = n_targeted * 50
revenue_saved = true_churners_caught * 1000 * 0.30 # We save 30% of them
profit = revenue_saved - cost

print(f"\n💰 BUSINESS IMPACT REPORT 💰")
print(f"Targeted Customers: {n_targeted}")
print(f"Campaign Cost: ${cost:,}")
print(f"Estimated Revenue Saved: ${revenue_saved:,}")
print(f"NET PROFIT from this Model: ${profit:,}")
import joblib
# Save the model
joblib.dump(best_model, 'pro_churn_model.pkl')
print("\n✅ Pro Model Saved as 'pro_churn_model.pkl'")