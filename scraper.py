import requests

URL = "https://www.multpl.com/shiller-pe/table/by-month"

resp = requests.get(URL, timeout=20)   # go get the page
resp.raise_for_status()                # crash if something went wrong

print("Status:", resp.status_code)
print("First 200 chars of the page:")
print(resp.text[:200])
