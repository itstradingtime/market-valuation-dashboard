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

# Make sure dates are in ascending order for a left to right timeline
df = df.sort_values("date", ascending=True)

# Show a preview to make sure the data looks right
print("Cleaned DataFrame preview:")
print(df.head())

# how info about data types to confirm our conversion worked
print("\nDataFrame info:")
df.info()

df.to_csv('data/shiller_pe.csv', index=False)

# Calculating rolling averages. 10 years = 120 months
df['avg_10y'] = df['shiller_pe'].rolling(window=120).mean()
# 30 years = 360 months
df['avg_30y'] = df['shiller_pe'].rolling(window=360).mean()
# Historical
df['avg_historical'] = df['shiller_pe'].expanding().mean()
# Historical median
df['median_historical'] = df['shiller_pe'].expanding().median()

average_pe_10y = df["avg_10y"].iloc[-1]   # last available 10-year rolling average
average_pe_30y = df["avg_30y"].iloc[-1]   # last available 30-year rolling average

print("\n--- Analysis ---")
# Get the most recent P/E (the first item in the 'shiller_pe' column)
current_pe = df['shiller_pe'].iloc[-1]

# Print our finding in a formatted way
print(f"Current Shiller P/E: {current_pe:.2f}")

# Calculate the average (mean) of the entire history
average_pe = df['shiller_pe'].mean()
print(f"Historical Average Shiller P/E: {average_pe:.2f}")

# Calculate the average (mean) of the last 30 years
print(f"30-Year Rolling Average P/E: {average_pe_30y:.2f}")

# Calculate the average (mean) of the last 10 years
print(f"10-Year Rolling Average P/E: {average_pe_10y:.2f}")

# Calculate the median of the entire history
median_pe = df["shiller_pe"].median()
print(f"Historical Median Shiller P/E: {median_pe:.2f}")

import os
from matplotlib import pyplot as plt

# Ensure a 'figures' folder exists to save the chart
os.makedirs("figures", exist_ok=True)

# Quick interpretation: are we above or below the long-term average, and median?
print("\nThe market is currently:")
print(compare_values(current_value=current_pe, historical_value=average_pe, name="historical average"))
print(compare_values(current_value=current_pe, historical_value=average_pe_30y, name="30 year average"))
print(compare_values(current_value=current_pe, historical_value=average_pe_10y, name="10 year average"))
print(compare_values(current_value=current_pe, historical_value=median_pe, name="historical median"))

from scipy import stats
percentile = stats.percentileofscore(df['shiller_pe'], current_pe)

print(f"\nCurrent Shiller P/E is higher than {percentile:.1f}% of all monthly readings.")

plt.figure(figsize=(10, 5))
plt.plot(df["date"], df["shiller_pe"], label="Shiller P/E")

# Add horizontal lines for our analysis
plt.plot(df["date"], df["avg_historical"], color='red', linestyle='--', label='Historical Avg')
plt.plot(df["date"], df["avg_30y"], color='orange', linestyle='--', label='30Y Rolling Avg')
plt.plot(df["date"], df["avg_10y"], color='purple', linestyle='--', label='10Y Rolling Avg')
plt.plot(df["date"], df["median_historical"], color='black', linestyle='--', label='Historical Median')

plt.title("Shiller P/E (CAPE) — Full History")
plt.xlabel("Date")
plt.ylabel("P/E")
plt.grid(True)
plt.legend()

# Save and show
plt.tight_layout()
plt.savefig("figures/shiller_pe_history.png", dpi=150)

# --- CHART 2: Zoomed-in view of the last 30 years ---

from datetime import timedelta

# Determine cutoff date (≈30 years ago)
cutoff_date = df["date"].max() - pd.DateOffset(years=30)

# Filter the dataframe
df_recent = df[df["date"] >= cutoff_date]

plt.figure(figsize=(10, 5))
plt.plot(df_recent["date"], df_recent["shiller_pe"], label="Shiller P/E", color="blue")
plt.plot(df_recent["date"], df_recent["avg_30y"], label="30Y Rolling Avg", color="orange")
plt.plot(df_recent["date"], df_recent["avg_10y"], label="10Y Rolling Avg", color="purple")

plt.title("Shiller P/E (CAPE) — Last 30 Years")
plt.xlabel("Date")
plt.ylabel("P/E")
plt.grid(True)
plt.legend()

# Save and show
plt.tight_layout()
plt.savefig("figures/shiller_pe_last30y.png", dpi=150)
plt.show()