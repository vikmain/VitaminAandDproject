import pandas as pd

# --- Load dataset and summary ---
df = pd.read_excel("data/Assignment_Dataset.xlsx", sheet_name="Dataset")
summary = pd.read_csv("outputs/summary.csv")

# --- Load codebook for facility mapping ---
codebook = pd.read_excel("data/Assignment_Dataset.xlsx", sheet_name="Codebook")
codebook.columns = codebook.columns.str.strip()

# Map facility codes to English names
mapping = dict(zip(codebook["Options"], codebook["label::English (en)"]))
df["Facility_Clean"] = df["health_facility"].map(mapping).fillna(df["health_facility"])

# --- Convert Age & Risk Score ---
df["q7"] = pd.to_numeric(df["q7"], errors="coerce")
df["q39"] = pd.to_numeric(df["q39"], errors="coerce")

# --- Apply filters ---
filtered = df[
    df["q2"].astype(str).str.contains("yes", case=False, na=False) &
    (df["q7"] > 30) &
    (df["q39"] > 3)
]

print("=== VALIDATION REPORT ===")

# 1. Check total filtered rows
expected_total = len(filtered)
reported_total = summary.loc[summary["Facility_Clean"] == "Total", "Persons Screened"].values[0]
print(f"Total rows passing filters: {expected_total} | Reported in summary: {reported_total} -> {'PASS' if expected_total == reported_total else 'FAIL'}")

# 2. Check facility counts
for facility in summary["Facility_Clean"].unique():
    if facility == "Total":
        continue
    actual_count = filtered[filtered["Facility_Clean"] == facility].shape[0]
    reported_count = summary.loc[summary["Facility_Clean"] == facility, "Persons Screened"].values[0]
    print(f"{facility}: actual={actual_count} | reported={reported_count} -> {'PASS' if actual_count == reported_count else 'FAIL'}")

# 3. Check percentages sum to 100
# 3. Check percentages sum to 100 (excluding Total row)
percent_sum = summary.loc[summary["Facility_Clean"] != "Total", "% Total Screened"].sum()
print(f"Percentage sum (excluding Total): {percent_sum:.2f} -> {'PASS' if abs(percent_sum - 100) < 0.01 else 'FAIL'}")


print("=== END REPORT ===")
