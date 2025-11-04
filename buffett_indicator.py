# Goal of this micro-step:
# - Connect to FRED
# - Download two quarterly series:
#     1) NCBEILQ027S (market cap proxy, millions of $)
#     2) GDP (nominal GDP, billions of $, SAAR)
# - Preview a few rows to confirm shape

from fredapi import Fred
import pandas as pd

# 1) Connect to FRED
# Easiest for now: paste your API key here (later we can use env vars)
FRED_API_KEY = "abf78da0eee3c8666bb3ce74ee12fca0"
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
