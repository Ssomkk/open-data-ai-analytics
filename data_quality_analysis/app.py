import os
import pandas as pd

# ── Paths: read from env vars (set by Docker), fall back to local relative paths ──
_HERE    = os.path.dirname(os.path.abspath(__file__))
_PROJECT = os.path.dirname(_HERE)

def _resolve(env_var: str, local_fallback: str) -> str:
    val = os.environ.get(env_var, "")
    if val and os.path.exists(val):
        return val
    return local_fallback

DATA_DIR = _resolve("DATA_DIR", os.path.join(_PROJECT, "data", "raw"))

RAW_XLSX   = os.path.join(DATA_DIR, "nuclear_safety_q4_2025.xlsx")
CLEAN_CSV  = os.path.join(DATA_DIR, "clean_data.csv")

print(f"Reading from: {RAW_XLSX}")
df = pd.read_excel(RAW_XLSX)

print(df.head())
print('df.shape ', df.shape)
print('df.describe')
print(df.describe())
print('nulls')
print(df.isna().sum())

# Create masks for each condition
mask1 = (df['station'] == 'ЗАЕС') & (df['year'] > 2022)
mask2 = (df['station'] == 'ЗАЕС') & (df['year'] == 2022) & (df['quarter'] == 4)

# Combine masks with OR (|) and then invert with NOT (~)
df = df[~(mask1 | mask2)]

print('column types')
print(df.dtypes)

df = df.replace('<', '', regex=True)
df = df.replace(',', '.', regex=True)
df = df.replace('ЮУАЕС', 'ПАЕС', regex=True)
df = df.drop(['iodine_ radionuclides_index'], axis=1)

cols = ['stable_ radionuclides_index', 'index_dump']
for col in cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

print(df.head())
print('column types')
print(df.dtypes)
print('df.describe')
print(df.describe())
print('nulls')
print(df.isna().sum())

print(f"Saving clean data to: {CLEAN_CSV}")
df.to_csv(CLEAN_CSV, index=False)
print("Done.")