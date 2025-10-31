import requests
import pandas as pd
from io import StringIO

URL = "https://www.multpl.com/shiller-pe/table/by-month"

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
if current_pe > average_pe:
    print("- ABOVE its historical average.")
elif current_pe == average_pe:
    print("- Same as its historical average.")
else:
    print("- BELOW its historical average.")

if current_pe > average_pe_30y:
    print("- ABOVE its 30 year average.")
elif current_pe == average_pe_30y:
    print("- Same as its 30 year average.")
else:
    print("- BELOW its 30 year average.")

if current_pe > average_pe_10y:
    print("- ABOVE its 10 year average.")
elif current_pe == average_pe_10y:
    print("- Same as its 10 year average.")
else:
    print("- BELOW its 10 year average.")

if current_pe > median_pe:
    print("- ABOVE its historical median.")
elif current_pe == median_pe:
    print("- Same as its historical median.")
else:
    print("- BELOW its historical median.")

from scipy import stats
percentile = stats.percentileofscore(df['shiller_pe'], current_pe)

print(f"\nCurrent Shiller P/E is higher than {percentile:.1f}% of all monthly readings.")
