import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier  # <-- NEW BRAIN
from sklearn.metrics import accuracy_score, classification_report

# 1. Load Data
df = pd.read_csv('customer_churn_data.csv')
X = df.drop(columns=['customer_id', 'is_churned'])
y = df['is_churned']

# 2. Split Data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Build the NEW Model
# n_estimators=100 means "Create 100 decision trees to vote"
model = RandomForestClassifier(n_estimators=100, random_state=42)

# 4. Train
print("Training the Random Forest...")
model.fit(X_train, y_train)

# 5. Predict
predictions = model.predict(X_test)

# 6. Evaluate
accuracy = accuracy_score(y_test, predictions)
print(f"\nNew Model Accuracy: {accuracy * 100:.2f}%")
print("\n--- Detailed Report ---")
print(classification_report(y_test, predictions))

# 7. Feature Importance (Why did it choose what it chose?)
# This tells us which clue was the most useful for the prediction
importances = pd.Series(model.feature_importances_, index=X.columns)
print("\n--- What Mattered Most? ---")
print(importances.sort_values(ascending=False))