# Goal of this micro-step:
# - Connect to FRED
# - Download two quarterly series:
#     1) NCBEILQ027S (market cap proxy, millions of $)
#     2) GDP (nominal GDP, billions of $, SAAR)
# - Preview a few rows to confirm shape

from fredapi import Fred
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
# 1) Connect to FRED
FRED_API_KEY = os.getenv("FRED_API_KEY")
fred = Fred(api_key=FRED_API_KEY)

# 2) Download both series (they come back as pandas Series with a DateTimeIndex)
mcap_millions = fred.get_series('NCBEILQ027S')   # market cap proxy, Q, millions $
gdp_billions  = fred.get_series('GDP')           # nominal GDP, Q, billions $, SAAR

# 3) Convert to DataFrame and align on dates (outer join, then we'll clean)
df = pd.concat(
    [
        mcap_millions.rename('mcap_millions'),
        gdp_billions.rename('gdp_billions')
    ],
    axis=1
)

# 4) Basic sanity checks
print("Head:\n", df.head())
print("\nTail:\n", df.tail())
print("\nNon-null counts:\n", df.notna().sum())

# --- Step 5: Clean & calculate the Buffett Indicator (% of GDP) ---

# Drop rows where one of the two series is missing
df = df.dropna(subset=['mcap_millions', 'gdp_billions'])

# Sort by date descending so the latest quarter is at the top
df = df.sort_index(ascending=False)

# Convert everything to billions for consistency
df['mcap_billions'] = df['mcap_millions'] / 1_000  # millions → billions

# Compute the Buffett Indicator ratio (market cap / GDP)
df['buffett_ratio'] = df['mcap_billions'] / df['gdp_billions'] * 100  # percent of GDP

# Rename and keep what matters
df = df[['mcap_billions', 'gdp_billions', 'buffett_ratio']]

# Print sanity checks
print("\n--- Computed Buffett Indicator ---")
print(df.head())

latest_value = df['buffett_ratio'].iloc[0]
print(f"\nLatest Buffett Indicator: {latest_value:.1f}% of GDP")

# Save clean dataset
df.to_csv('data/buffett_indicator.csv', index_label='date')
print("\nSaved to data/buffett_indicator.csv")

