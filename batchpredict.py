import pandas as pd
import numpy as np
import joblib

# 1. GENERATE NEW DATA (Simulating the "New Customer List")
# Imagine the Sales Team just sent you this list of 500 people.
np.random.seed(999) # New random seed = New people
n_new = 500

new_data = pd.DataFrame({
    'customer_id': np.arange(2001, 2001 + n_new),
    'age': np.random.randint(18, 70, size=n_new),
    'monthly_bill': np.random.randint(20, 120, size=n_new),
    'support_tickets': np.random.randint(0, 10, size=n_new)
})

print(f"--- Loaded {n_new} New Customers ---")

# 2. LOAD THE SAVED BRAIN
model = joblib.load('churn_model.pkl')
print("--- Model Loaded Successfully ---")

# 3. PREDICT EVERYONE INSTANTLY
# We don't need a loop. The model can process 500 rows in milliseconds.
predictions = model.predict(new_data[['age', 'monthly_bill', 'support_tickets']])
probabilities = model.predict_proba(new_data[['age', 'monthly_bill', 'support_tickets']])

# 4. ADD PREDICTIONS TO THE TABLE
new_data['churn_prediction'] = predictions
new_data['risk_score'] = probabilities[:, 1] # The probability of Churn (0-1)

# 5. FILTER: FIND THE "AT RISK" CUSTOMERS
# We only want to bug the sales team about people who are > 80% likely to leave.
high_risk_list = new_data[new_data['risk_score'] > 0.80]

# 6. SAVE THE "HIT LIST" TO EXCEL/CSV
high_risk_list.to_csv('high_risk_customers.csv', index=False)

print(f"\n✅ DONE! Found {len(high_risk_list)} high-risk customers.")
print("Saved list to 'high_risk_customers.csv'.")
print("\n--- PREVIEW OF THE HIT LIST ---")
print(high_risk_list.head())