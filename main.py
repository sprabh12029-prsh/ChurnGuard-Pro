import pandas as pd
import numpy as np

np.random.seed(42)
n_customers = 1000

# 1. Generate Random Data
ids = np.arange(1001, 1001 + n_customers)
ages = np.random.randint(18, 70, size=n_customers)
bills = np.random.randint(20, 120, size=n_customers)
tickets = np.random.randint(0, 10, size=n_customers)

# 2. CREATE A STRONG PATTERN (The "Signal")
# We start with a base churn chance of 0%
churn_probability = np.zeros(n_customers)

# Rule 1: If they have more than 5 tickets, boost churn chance by 70%
churn_probability += np.where(tickets > 5, 0.70, 0)

# Rule 2: If bill is over $100, boost churn chance by 30%
churn_probability += np.where(bills > 100, 0.30, 0)

# Rule 3: Add a tiny bit of random noise (so it's not "too" perfect)
churn_probability += np.random.normal(0, 0.1, n_customers)

# 3. Finalize the Churn (0 or 1)
# Clip probability to stay between 0 and 1
churn_probability = np.clip(churn_probability, 0, 1)
is_churned = np.random.binomial(1, churn_probability)

# 4. Save
df = pd.DataFrame({
    'customer_id': ids,
    'age': ages, # This is still random noise! Let's see if the model learns to ignore it.
    'monthly_bill': bills,
    'support_tickets': tickets,
    'is_churned': is_churned
})

df.to_csv('customer_churn_data.csv', index=False)
print("New 'Clean' Dataset Created!")