import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib # Tool for saving/loading models

# --- PART 1: RETRAIN & SAVE THE MODEL ---
# (We do this to make sure we have the latest version saved)
df = pd.read_csv('customer_churn_data.csv')
X = df.drop(columns=['customer_id', 'is_churned'])
y = df['is_churned']

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Save the model to a file (like saving a Word doc)
joblib.dump(model, 'churn_model.pkl')
print("Model saved as 'churn_model.pkl'!")

# --- PART 2: THE PREDICTION APP ---
print("\n--- NEW CUSTOMER PREDICTOR ---")
print("Enter the details of the customer you want to check:")

# Ask the user for inputs
# We need to type convert inputs to integers (int) or floats
age = int(input("Customer Age (e.g., 30): "))
bill = float(input("Monthly Bill (e.g., 50.50): "))
tickets = int(input("Support Tickets (0-10): "))

# Create a mini-table for just this one person
new_customer = pd.DataFrame({
    'age': [age],
    'monthly_bill': [bill],
    'support_tickets': [tickets]
})

# Load the saved model and predict
loaded_model = joblib.load('churn_model.pkl')
prediction = loaded_model.predict(new_customer)
probability = loaded_model.predict_proba(new_customer)

print("\n--- RESULTS ---")
if prediction[0] == 1:
    print(f"⚠️ RISK ALERT: This customer is likely to CHURN.")
    print(f"Confidence: {probability[0][1] * 100:.1f}%")
else:
    print(f"✅ SAFE: This customer is likely to STAY.")
    print(f"Confidence: {probability[0][0] * 100:.1f}%")