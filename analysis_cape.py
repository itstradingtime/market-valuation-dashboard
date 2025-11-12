# analysis_cape.py  (minimal, clean)
import pandas as pd
from pathlib import Path
from matplotlib import pyplot as plt

# 1) Load the clean CSV produced by cape_from_source.py
csv_path = Path("data/shiller_cape_series.csv")
if not csv_path.exists():
    raise FileNotFoundError("Run cape_from_source.py first to create data/shiller_cape_series.csv")

df = pd.read_csv(csv_path, parse_dates=["date"]).sort_values("date").reset_index(drop=True)

# 2) Quick sanity check
print("Rows:", len(df))
print("Last row:\n", df.tail(1).to_string(index=False))  # should show current month (e.g., 2025-11-01)

# 3) One simple chart
Path("figures").mkdir(exist_ok=True)
plt.figure(figsize=(10, 5))
plt.plot(df["date"], df["shiller_pe"], label="Shiller P/E (CAPE)")
plt.title("Shiller P/E (CAPE) — Full History")
plt.xlabel("Date"); plt.ylabel("P/E"); plt.grid(True); plt.legend()
plt.tight_layout()
plt.savefig("figures/shiller_pe_history.png", dpi=150)
print("Saved figures/shiller_pe_history.png")
