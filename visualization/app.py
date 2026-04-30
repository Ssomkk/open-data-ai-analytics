import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

plt.style.use('default')

# ── Paths ─────────────────────────────────────────────────────────────────────
_HERE    = os.path.dirname(os.path.abspath(__file__))
_PROJECT = os.path.dirname(_HERE)

def _resolve(env_var: str, local_fallback: str) -> str:
    val = os.environ.get(env_var, "")
    if val and os.path.exists(val):
        return val
    return local_fallback

DATA_DIR    = _resolve("DATA_DIR",    os.path.join(_PROJECT, "data", "raw"))
REPORTS_DIR = _resolve("REPORTS_DIR", os.path.join(_PROJECT, "reports", "lab1"))
FIGURES_DIR = os.path.join(REPORTS_DIR, "figures")
os.makedirs(FIGURES_DIR, exist_ok=True)

CLEAN_CSV = os.path.join(DATA_DIR, "clean_data.csv")
print(f"Reading: {CLEAN_CSV}")

# Load data
df = pd.read_csv(CLEAN_CSV)

# ---- Fix 1: aggregate by year (otherwise plot is noisy and wrong) ----
yearly = df.groupby('year')[['cs_137_emission', 'co_60_ emission']].mean().reset_index()

# Emission dynamics
plt.figure(figsize=(10, 6))
plt.plot(yearly['year'], yearly['cs_137_emission'], label='Cs-137', marker='o')
plt.plot(yearly['year'], yearly['co_60_ emission'], label='Co-60', marker='s')

plt.title('Динаміка викидів за роками (дослідження)')
plt.xlabel('Рік')
plt.ylabel('Обсяг викидів, ТБк')
plt.legend()
plt.grid(True)

plt.savefig('reports/lab1/figures/emission_dynamics.png')
plt.close()

# ---- Boxplot ----
plt.figure(figsize=(10, 6))
sns.boxplot(data=df, x='station', y='irg')

plt.title('Порівняння радіаційного фону по АЕС')
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig('reports/lab1/figures/irg_stations.png')
plt.close()

