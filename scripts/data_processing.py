# Import the required library files 
import pandas as pd
from datetime import datetime

# Decalre the log function fo
def log(message):
    print(f"[INFO {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}")

# Load the given dataset 
log("Loading dataset...")
df = pd.read_excel("data/Assignment_Dataset.xlsx", sheet_name="Dataset")
df.columns = df.columns.str.strip()
log(f"Dataset loaded with {len(df)} rows and {len(df.columns)} columns")

# Load the codebook
log("Loading codebook...")
codebook = pd.read_excel("data/Assignment_Dataset.xlsx", sheet_name="Codebook")
codebook.columns = codebook.columns.str.strip()
log(f"Codebook loaded with {len(codebook)} rows and {len(codebook.columns)} columns")

# Create the Facility Mapping Options English name
if "Options" in codebook.columns and "label::English (en)" in codebook.columns:
    mapping = dict(zip(codebook["Options"], codebook["label::English (en)"]))
    df["Facility_Clean"] = df["health_facility"].map(mapping).fillna(df["health_facility"])
    log("Facility mapping applied (codes mapped to English names)")
else:
    raise ValueError("Expected 'Options' and 'label::English (en)' columns not found in Codebook")

# Convert Age & Risk Score to Numeric
log("Converting Age (q7) and Risk Score (q39) to numeric...")
df["q7"] = pd.to_numeric(df["q7"], errors="coerce")   # Age
df["q39"] = pd.to_numeric(df["q39"], errors="coerce") # Risk Score

# Filtering Logic as per the given conditions
log("Applying filters: Consent=Yes, Age>30, Risk Score>3...")
filtered = df[
    df["q2"].astype(str).str.contains("yes", case=False, na=False) &  # Consent = yes
    (df["q7"] > 30) &                                                 # Age > 30
    (df["q39"] > 3)                                                   # Risk Score > 3
]
log(f"Filtered dataset has {len(filtered)} rows")

# Aggregation on the provided facilites
target_facilities = [
    "CHC Harsana", "CHC Laxmangarh", "CHC Pinan", "CHC Rajgarh", "CHC Tahla",
    "PHC Bahatukala", "PHC Bhanokhar", "PHC Dhamred", "PHC Ramanagar"
]
# Display the table 
log("Generating summary table...")
summary = (
    filtered[filtered["Facility_Clean"].isin(target_facilities)]
    .groupby("Facility_Clean")
    .size()
    .reset_index(name="Persons Screened")
)
# When total screened is not provided 
if not summary.empty:
    summary["% Total Screened"] = (summary["Persons Screened"] / summary["Persons Screened"].sum()) * 100
    total_row = pd.DataFrame({
        "Facility_Clean": ["Total"],
        "Persons Screened": [summary["Persons Screened"].sum()],
        "% Total Screened": [100.0]
    })
    summary = pd.concat([summary, total_row], ignore_index=True)
else:
    log("No facilities matched after filtering. All counts are zero.")
    summary = pd.DataFrame(columns=["Facility_Clean", "Persons Screened", "% Total Screened"])

# Display the output and save it into the summary.csv file 
summary.to_csv("outputs/summary.csv", index=False)
log("Summary table saved to summary.csv")
log("Final summary table:")
print(summary.head(20))

# Debugging: print actual facility names , it used to varify the result
print("Sample Facility_Clean values:", filtered["Facility_Clean"].dropna().unique()[:20])
