import requests
import pandas as pd
from io import StringIO

URL = "https://www.multpl.com/shiller-pe/table/by-month"

def compare_values(current_value, historical_value, name):
    """Compare a current value to the historical value and returns a formatted string."""
    if current_value > historical_value:
        return f"- ABOVE its {name}."
    elif current_value == historical_value:
        return f"- SAME as its {name}."
    else:
        return f"- BELOW its {name}."

resp = requests.get(URL, timeout=20)   # go get the page
resp.raise_for_status()                # crash if something went wrong

tables = pd.read_html(StringIO(resp.text))       # Use pandas to read the HTML we fetched
df = tables[0]                         # Get the first table from the list


# Rename the columns to something clean and consistent
df.columns = ['date', 'shiller_pe']

# Convert the 'date' column from text to datetime objects
df['date'] = pd.to_datetime(df['date'])

# Show a preview to make sure the data looks right
print("Cleaned DataFrame preview:")
print(df.head())

# how info about data types to confirm our conversion worked
print("\nDataFrame info:")
df.info()

df.to_csv('data/shiller_pe.csv', index=False)

print("\n--- Analysis ---")
# Get the most recent P/E (the first item in the 'shiller_pe' column)
current_pe = df['shiller_pe'].iloc[0]

# Print our finding in a formatted way
print(f"Current Shiller P/E: {current_pe:.2f}")

# Calculate the average (mean) of the entire history
average_pe = df['shiller_pe'].mean()
print(f"Historical Average Shiller P/E: {average_pe:.2f}")

# Calculate the average of the last 30 years
thirty_years_ago = df['date'].max() - pd.DateOffset(years=30)
df_30_years = df[df['date'] > thirty_years_ago]
average_pe_30y = df_30_years['shiller_pe'].mean()
print(f"30 year Average Shiller P/E: {average_pe_30y:.2f}")

# Calculate the average of the last 10 years
ten_years_ago = df['date'].max() - pd.DateOffset(years=10)
df_10_years = df[df['date'] > ten_years_ago]
average_pe_10y = df_10_years['shiller_pe'].mean()
print(f"10 year Average Shiller P/E: {average_pe_10y:.2f}")

# Calculate the median of the entire history
median_pe = df["shiller_pe"].median()
print(f"Historical Median Shiller P/E: {median_pe:.2f}")

# Quick interpretation: are we above or below the long-term average, and median?
print("\nThe market is currently:")
print(compare_values(current_value=current_pe, historical_value=average_pe, name="historical average"))
print(compare_values(current_value=current_pe, historical_value=average_pe_30y, name="30 year average"))
print(compare_values(current_value=current_pe, historical_value=average_pe_10y, name="10 year average"))
print(compare_values(current_value=current_pe, historical_value=median_pe, name="historical median"))

from scipy import stats
percentile = stats.percentileofscore(df['shiller_pe'], current_pe)

print(f"\nCurrent Shiller P/E is higher than {percentile:.1f}% of all monthly readings.")

import os
from matplotlib import pyplot as plt

# Ensure a 'figures' folder exists to save the chart
os.makedirs("figures", exist_ok=True)

# Make sure dates are in ascending order for a left to right timeline
df = df.sort_values("date", ascending=True)

plt.figure(figsize=(10, 5))
plt.plot(df["date"], df["shiller_pe"], label="Shiller P/E")

# Add horizontal lines for our analysis
plt.axhline(y=average_pe, color='red', linestyle='--', label=f'Hist. Avg: {average_pe:.2f}')
plt.axhline(y=average_pe_30y, color='orange', linestyle='--', label=f'30Y Avg: {average_pe_30y:.2f}')
plt.axhline(y=average_pe_10y, color='purple', linestyle='--', label=f'10Y Avg: {average_pe_10y:.2f}')
plt.axhline(y=median_pe, color='green', linestyle='--', label=f'Median: {median_pe:.2f}')

plt.title("Shiller P/E (CAPE) — Full History")
plt.xlabel("Date")
plt.ylabel("P/E")
plt.grid(True)
plt.legend()

# Save and show
plt.tight_layout()
plt.savefig("figures/shiller_pe_history.png", dpi=150)
plt.show()