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
