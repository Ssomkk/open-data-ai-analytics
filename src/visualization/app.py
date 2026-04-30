import os
import json
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

plt.style.use('default')

# ── Paths ─────────────────────────────────────────────────────────────────────
_HERE    = os.path.dirname(os.path.abspath(__file__))
_PROJECT = os.path.dirname(_HERE)

def _resolve(env_var: str, local_fallback: str) -> str:
    val = os.environ.get(env_var, "")
    if val and os.path.exists(os.path.dirname(val)):
        return val
    return local_fallback

DATA_DIR    = _resolve("DATA_DIR",    os.path.join(_PROJECT, "data", "raw"))
REPORTS_DIR = _resolve("REPORTS_DIR", os.path.join(_PROJECT, "reports", "lab1"))
FIGURES_DIR = os.path.join(REPORTS_DIR, "figures")
os.makedirs(FIGURES_DIR, exist_ok=True)

print(f"[visualization] DATA_DIR: {DATA_DIR}")
print(f"[visualization] REPORTS_DIR: {REPORTS_DIR}")
print(f"[visualization] FIGURES_DIR: {FIGURES_DIR}")

CLEAN_CSV = os.path.join(DATA_DIR, "clean_data.csv")
VIZ_REPORT = os.path.join(REPORTS_DIR, "visualization_report.json")

print(f"Reading: {CLEAN_CSV}")

# Load data
df = pd.read_csv(CLEAN_CSV)

print(f"\n[visualization] Generating visualizations...")
print(f"Shape: {df.shape}")

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

plt.savefig(os.path.join(FIGURES_DIR, 'emission_dynamics.png'))
plt.close()
print("emission_dynamics.png")

# ---- Boxplot ----
plt.figure(figsize=(10, 6))
sns.boxplot(data=df, x='station', y='irg')

plt.title('Порівняння радіаційного фону по АЕС')
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(os.path.join(FIGURES_DIR, 'irg_stations.png'))
plt.close()
print("irg_stations.png")

# ── Generate Visualization Report ──────────────────────────────────────────────
print(f"\n[visualization] Generating visualization report...")

viz_report = {
    "metadata": {
        "module": "visualization",
        "version": "1.0"
    },
    "summary": {
        "total_rows": int(df.shape[0]),
        "total_columns": int(df.shape[1]),
    },
    "charts": {
        "emission_dynamics": {
            "type": "line_plot",
            "description": "Average Cs-137 and Co-60 emission by year",
            "x_axis": "year",
            "y_axis": "emission (TBq)",
            "file": "emission_dynamics.png"
        },
        "irg_stations": {
            "type": "boxplot",
            "description": "Radiation background (IRG) by nuclear station",
            "x_axis": "station",
            "y_axis": "IRG index",
            "file": "irg_stations.png"
        }
    },
    "files_generated": [
        "emission_dynamics.png",
        "irg_stations.png"
    ]
}

# Save to JSON
with open(VIZ_REPORT, 'w', encoding='utf-8') as f:
    json.dump(viz_report, f, indent=2, ensure_ascii=False)

print(f"Visualization report saved to: {VIZ_REPORT}")
print(f"\nVisualization Summary:")
print(f"  - Charts generated: {len(viz_report['charts'])}")
print(f"  - Files: {viz_report['files_generated']}")

print("\n[visualization] Done.")
