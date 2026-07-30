import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv("group_1_expenses.csv", parse_dates=["created_at"])
print("--- DataFrame Info ---")
print(df.info())

print("\n--- DataFrame Describe ---")
print(df.describe())

# 2. Groupby Category & Groupby Payer
print("\n--- Total Spend per Category ---")
category_spend = df.groupby("category")["amount_cents"].sum()
print(category_spend)

print("\n--- Total Paid per Payer ---")
# Note: Ensure your CSV includes a 'paid_by' or payer name column
payer_spend = df.groupby("paid_by")["amount_cents"].sum()
print(payer_spend)

# 4. Monthly Spend Over Time & Charts
# Extract Year-Month for grouping
df["year_month"] = df["created_at"].dt.to_period("M")
monthly_spend = df.groupby("year_month")["amount_cents"].sum()

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Line chart: Monthly spend over time
monthly_spend.plot(kind="line", ax=axes[1], marker="o", color="orange", title="Monthly Spend Over Time")
axes[1].set_ylabel("Cents")