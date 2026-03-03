import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Load the data we created earlier
df = pd.read_csv('customer_churn_data.csv')

# 2. "Sanity Check" - Look at the data summary in the terminal
print("--- Data Info ---")
print(df.info()) 
print("\n--- Statistics ---")
print(df.describe()) 

# 3. Visualization 1: Count of Churned vs Retained
# This helps us see if the dataset is "imbalanced"
plt.figure(figsize=(6, 4))
sns.countplot(x='is_churned', data=df)
plt.title('Count of Churned vs. Retained Customers')
print("\nGraph 1 generated: Close the popup window to see the next one.")
plt.show() 

# 4. Visualization 2: Monthly Bill vs Churn
# Do people with higher bills leave more often?
plt.figure(figsize=(6, 4))
sns.boxplot(x='is_churned', y='monthly_bill', data=df)
plt.title('Monthly Bill Distribution by Churn Status')
print("Graph 2 generated.")
plt.show()