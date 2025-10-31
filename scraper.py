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

# Calculate the median of the entire history
median_pe = df["shiller_pe"].median()
print(f"Historical Median Shiller P/E: {median_pe:.2f}")

# Quick interpretation: are we above or below the long-term average, and median?
if current_pe > average_pe:
    print("→ The market is currently ABOVE its historical average.")
else:
    print("→ The market is currently BELOW its historical average.")

if current_pe > median_pe:
    print("→ The market is currently ABOVE its historical median.")
else:
    print("→ The market is currently BELOW its historical median.")