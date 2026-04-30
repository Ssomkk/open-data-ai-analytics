import os
import json
import pandas as pd

# ── Paths: read from env vars (set by Docker), fall back to local relative paths ──
_HERE    = os.path.dirname(os.path.abspath(__file__))
_PROJECT = os.path.dirname(_HERE)

def _resolve(env_var: str, local_fallback: str) -> str:
    val = os.environ.get(env_var, "")
    if val and os.path.exists(os.path.dirname(val)):
        return val
    return local_fallback

DATA_DIR    = _resolve("DATA_DIR",    os.path.join(_PROJECT, "data", "raw"))
REPORTS_DIR = _resolve("REPORTS_DIR", os.path.join(_PROJECT, "reports", "lab1"))

# Ensure directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)

print(f"[data_quality] DATA_DIR: {DATA_DIR}")
print(f"[data_quality] REPORTS_DIR: {REPORTS_DIR}")

RAW_XLSX   = os.path.join(DATA_DIR, "nuclear_safety_q4_2025.xlsx")
CLEAN_CSV  = os.path.join(DATA_DIR, "clean_data.csv")
QUALITY_REPORT = os.path.join(REPORTS_DIR, "quality_report.json")

print(f"Reading from: {RAW_XLSX}")
df = pd.read_excel(RAW_XLSX)

print("\n=== INITIAL DATA QUALITY ===")
print(df.head())
print(f"\nShape: {df.shape}")
print(f"\nData types:\n{df.dtypes}")
print(f"\nNull values:\n{df.isna().sum()}")

# Create masks for each condition
mask1 = (df['station'] == 'ЗАЕС') & (df['year'] > 2022)
mask2 = (df['station'] == 'ЗАЕС') & (df['year'] == 2022) & (df['quarter'] == 4)

# Combine masks with OR (|) and then invert with NOT (~)
df = df[~(mask1 | mask2)]

print("\n=== AFTER FILTERING ===")
print(f"Shape: {df.shape}")

df = df.replace('<', '', regex=True)
df = df.replace(',', '.', regex=True)
df = df.replace('ЮУАЕС', 'ПАЕС', regex=True)
df = df.drop(['iodine_ radionuclides_index'], axis=1)

cols = ['stable_ radionuclides_index', 'index_dump']
for col in cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

print("\n=== FINAL DATA QUALITY ===")
print(df.head())
print(f"\nData types:\n{df.dtypes}")
print(f"\nDescriptive statistics:\n{df.describe()}")
print(f"\nNull values:\n{df.isna().sum()}")

print(f"\nSaving clean data to: {CLEAN_CSV}")
df.to_csv(CLEAN_CSV, index=False)
print("✓ CSV saved")

# ── Generate Quality Report ────────────────────────────────────────────────────
print(f"\nGenerating quality report...")

quality_report = {
    "metadata": {
        "module": "data_quality_analysis",
        "version": "1.0"
    },
    "rows": int(df.shape[0]),
    "columns": int(df.shape[1]),
    "column_names": list(df.columns),
    "missing_values": {col: int(df[col].isna().sum()) for col in df.columns},
    "missing_total": int(df.isna().sum().sum()),
    "duplicates": int(df.duplicated().sum()),
    "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
    "describe": df.describe(include='all').round(4).to_dict(),
}

# Save to JSON
with open(QUALITY_REPORT, 'w', encoding='utf-8') as f:
    json.dump(quality_report, f, indent=2, ensure_ascii=False)

print(f"✓ Quality report saved to: {QUALITY_REPORT}")
print(f"\nQuality Summary:")
print(f"  - Total rows: {quality_report['rows']}")
print(f"  - Total columns: {quality_report['columns']}")
print(f"  - Missing values: {quality_report['missing_total']}")
print(f"  - Duplicates: {quality_report['duplicates']}")

print("\n[data_quality] Done.")
