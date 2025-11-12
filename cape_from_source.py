import pandas as pd
from pathlib import Path

src = Path("data/ie_data.xls")
print(f"Loading: {src.as_posix()}")

# 1. Load the raw data
df_raw = pd.read_excel(src, sheet_name="Data", header=7, engine="xlrd")

# 2. Let's see all the column names (this time, all 22)
print("--- All Column Names ---")
print(list(df_raw.columns))

# 3. Detect the CAPE column robustly (handles CAPE / CAPE.1, etc.)
cape_col = next((c for c in df_raw.columns if str(c).strip().upper().startswith("CAPE")), None)
if cape_col is None:
    raise RuntimeError("Could not find a CAPE column in the sheet. Print columns and check.")

cols_to_keep = {
    "Date": "date",
    cape_col: "shiller_pe",
}


# 4. Select and rename
df = df_raw[cols_to_keep.keys()].rename(columns=cols_to_keep)

# 5–6. Robust parse 'YYYY.M' / 'YYYY.MM' → YYYY-mm-01
parts = df["date"].astype(str).str.split(".", n=1, expand=True)
year = parts[0]
raw = parts[1].fillna("").str.replace(r"\D", "", regex=True)

# Special-case Oct: '.1' -> '10'; pad single digits; keep first two chars
month = raw.where(raw != "1", "10")
month = month.where(month.str.len() != 1, "0" + month)
month = month.str.slice(0, 2)

df["date"] = pd.to_datetime(year + "-" + month + "-01", errors="coerce")


# 7. Clean and validate data
# Make sure shiller_pe is a number
df["shiller_pe"] = pd.to_numeric(df["shiller_pe"], errors="coerce")

# Drop any rows where the date or the PE is invalid
df = df.dropna(subset=["date", "shiller_pe"])
df = df.drop_duplicates(subset="date").sort_values("date").reset_index(drop=True)

print("\n--- Final Cleaned Data (Your Simple Way) ---")
print(df.head(3))
print(df.tail(3))

# Validate latest month and save for the dashboard
print("\nLast row (should be current month):")
print(df.tail(1).to_string(index=False))

out = Path("data/shiller_cape_series.csv")
df.to_csv(out, index=False)
print(f"Saved {len(df):,} rows to {out.as_posix()}")

# --- Quick chart for the dashboard ---
from matplotlib import pyplot as plt
charts_dir = Path("charts"); charts_dir.mkdir(exist_ok=True)
s = pd.read_csv("data/shiller_cape_series.csv", parse_dates=["date"])
ax = s.plot(x="date", y="shiller_pe", legend=False)
ax.set_title("Shiller CAPE (updated daily within month)")
ax.set_xlabel(""); ax.set_ylabel("CAPE")
plt.tight_layout()
plt.savefig(charts_dir / "cape_line.png", dpi=150)
print(f"Chart saved to {charts_dir/'cape_line.png'}")
