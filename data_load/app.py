import requests
import os
import sqlite3
import pandas as pd

# ── Paths ─────────────────────────────────────────────────────────────────────
_HERE    = os.path.dirname(os.path.abspath(__file__))
_PROJECT = os.path.dirname(_HERE)

def _resolve(env_var: str, local_fallback: str) -> str:
    """Use env var only when the path exists; otherwise use local fallback."""
    val = os.environ.get(env_var, "")
    if val and os.path.exists(os.path.dirname(val)):
        return val
    return local_fallback

DATA_DIR = _resolve("DATA_DIR", os.path.join(_PROJECT, "data", "raw"))
DB_PATH  = _resolve("DB_PATH",  os.path.join(_PROJECT, "data", "nuclear_safety.db"))

# Папка для сирих даних
RAW_DIR = DATA_DIR

# Створюємо директорію, якщо її немає
os.makedirs(RAW_DIR, exist_ok=True)

print(f"[data_load] DATA_DIR: {DATA_DIR}")
print(f"[data_load] DB_PATH: {DB_PATH}")

# Список прямих URL на файли
urls = [
    "https://data.gov.ua/dataset/c445c6ea-f0c3-4167-abb1-5afb4a0e5499/resource/afa0c772-2554-4b9a-98b4-980e54b1e21a/download/pasport-naboru-danikh.xlsx",
    "https://data.gov.ua/dataset/c445c6ea-f0c3-4167-abb1-5afb4a0e5499/resource/d55eebcf-4660-4919-96b3-4894be5a6cda/download/nuclear_safety_q4_2025.xlsx",
]

for url in urls:
    filename = url.split("/")[-1]
    filepath = os.path.join(RAW_DIR, filename)

    print(f"Downloading {filename} ...")
    r = requests.get(url)

    if r.status_code == 200:
        with open(filepath, "wb") as f:
            f.write(r.content)
        print(f"Saved to {filepath}")
    else:
        print(f"Failed to download {url} (status {r.status_code})")

# ── Database Creation ──────────────────────────────────────────────────────────
print("\n[data_load] Creating SQLite database...")

try:
    # Read the XLSX file
    xlsx_path = os.path.join(RAW_DIR, "nuclear_safety_q4_2025.xlsx")
    if os.path.exists(xlsx_path):
        print(f"Reading {xlsx_path}...")
        df = pd.read_excel(xlsx_path)

        # Create/connect to SQLite database
        conn = sqlite3.connect(DB_PATH)
        print(f"Database created/connected: {DB_PATH}")

        # Create table and import data
        table_name = "nuclear_safety"
        df.to_sql(table_name, conn, if_exists='replace', index=False)

        print(f"✓ Table '{table_name}' created with {len(df)} records")
        print(f"✓ Columns: {list(df.columns)}")

        conn.close()
        print(f"✓ Database saved to {DB_PATH}")
    else:
        print(f"Warning: {xlsx_path} not found. Cannot create database.")
except Exception as e:
    print(f"✗ Error creating database: {e}")

print("\n[data_load] Done.")
