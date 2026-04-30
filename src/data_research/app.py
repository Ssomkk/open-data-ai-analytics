import os
import json
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
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

print(f"[data_research] DATA_DIR: {DATA_DIR}")
print(f"[data_research] REPORTS_DIR: {REPORTS_DIR}")
print(f"[data_research] FIGURES_DIR: {FIGURES_DIR}")

CLEAN_CSV = os.path.join(DATA_DIR, "clean_data.csv")
RESEARCH_REPORT = os.path.join(REPORTS_DIR, "research_report.json")

print(f"Reading: {CLEAN_CSV}")

# Load data
df = pd.read_csv(CLEAN_CSV)

print("\n=== DATA LOADED ===")
print(f"Shape: {df.shape}")
print("Missing values:\n", df.isna().sum())
print("\nData types:\n", df.dtypes)

# Fill missing values
df['co_60_dump'] = df['co_60_dump'].fillna(df['co_60_dump'].mean())

print("\nMissing values after fill:\n", df.isna().sum())

# Columns for histogram
columns = [
    'irg', 'irg_index',
    'iodine_ radionuclides',
    'stable_radionuclides', 'stable_ radionuclides_index',
    'cs_137_emission', 'co_60_ emission',
    'cs_137_dump', 'co_60_dump',
    'volume', 'index_radioactive_releas', 'index_dump'
]

# Histograms
print(f"\n[data_research] Generating histograms...")
n_cols = 3
n_rows = (len(columns) + n_cols - 1) // n_cols

fig, axes = plt.subplots(n_rows, n_cols, figsize=(12, 4 * n_rows))
axes = axes.flatten()

for i, column in enumerate(columns):
    df[column].hist(ax=axes[i])
    axes[i].set_title(column)

for j in range(i + 1, len(axes)):
    axes[j].set_visible(False)

plt.tight_layout()
plt.savefig(os.path.join(FIGURES_DIR, 'data_distributions.png'))
plt.close()
print("data_distributions.png")

# Avg cs-137 emission by year
avg_cs137 = df.groupby('year')['cs_137_emission'].mean()
plt.figure()
plt.plot(avg_cs137)
plt.title('Average cs_137_emission by year')
plt.savefig(os.path.join(FIGURES_DIR, 'cs_137_emission_by_year.png'))
plt.close()
print("cs_137_emission_by_year.png")

# Avg co-60 emission by year
avg_co60 = df.groupby('year')['co_60_ emission'].mean()
plt.figure()
plt.plot(avg_co60)
plt.title('Average co_60_emission by year')
plt.savefig(os.path.join(FIGURES_DIR, 'co_60_emission_by_year.png'))
plt.close()
print("co_60_emission_by_year.png")

# IRG by station
station_irg = df.groupby('station')['irg'].mean()
stations = df['station'].unique()

plt.figure()
plt.bar(stations, station_irg)
plt.savefig(os.path.join(FIGURES_DIR, 'avg_irg_by_station.png'))
plt.close()
print("avg_irg_by_station.png")

# IRG index by station
station_irg_indx = df.groupby('station')['irg_index'].mean()

plt.figure()
plt.bar(stations, station_irg_indx)
plt.savefig(os.path.join(FIGURES_DIR, 'avg_irg_indx_by_station.png'))
plt.close()
print("avg_irg_indx_by_station.png")

# Scatter plots
plt.figure()
plt.scatter(df['cs_137_dump'], df['volume'])
plt.title('cs_137_dump vs volume')
plt.savefig(os.path.join(FIGURES_DIR, 'cs137_dump_vs_volume.png'))
plt.close()
print("cs137_dump_vs_volume.png")

plt.figure()
plt.scatter(df['co_60_dump'], df['volume'])
plt.title('co_60_dump vs volume')
plt.savefig(os.path.join(FIGURES_DIR, 'co60_dump_vs_volume.png'))
plt.close()
print("co60_dump_vs_volume.png")

plt.figure()
plt.scatter(df['cs_137_dump'], df['cs_137_emission'])
plt.title('cs_137_dump vs cs_137_emission')
plt.savefig(os.path.join(FIGURES_DIR, 'cs137_dump_vs_emission.png'))
plt.close()
print("cs137_dump_vs_emission.png")

# Filtered scatter (specific station)
mask = df['station'] == 'ХАЕС'

plt.figure()
plt.scatter(df.loc[mask, 'co_60_ emission'], df.loc[mask, 'irg'])
plt.title('co_60_emission vs irg (ХАЕС only)')
plt.savefig(os.path.join(FIGURES_DIR, 'co60_vs_irg_haes.png'))
plt.close()
print("co60_vs_irg_haes.png")

# PCA
df_scaled = df.drop(['station'], axis=1)

scaler = StandardScaler()
df_scaled = scaler.fit_transform(df_scaled)

pca = PCA(0.90)
df_pca = pca.fit_transform(df_scaled)

print("\nExplained variance ratio:\n", pca.explained_variance_ratio_)

plt.figure()
plt.scatter(df_pca[:, 0], df_pca[:, 1])
plt.title('PCA (first 2 components)')
plt.savefig(os.path.join(FIGURES_DIR, 'pca_2d.png'))
plt.close()
print("pca_2d.png")

# Correlation heatmap
df_corr = df.drop(['station'], axis=1)
corr_matr = df_corr.corr()

plt.figure(figsize=(20, 10))
sns.heatmap(corr_matr, annot=True, cmap='coolwarm', fmt=".2f", square=True)
plt.title('Correlation Matrix Heatmap')
plt.tight_layout()
plt.savefig(os.path.join(FIGURES_DIR, 'correlation_matrix.png'))
plt.close()
print("correlation_matrix.png")

# ── Generate Research Report ──────────────────────────────────────────────────
print(f"\n[data_research] Generating research report...")

# Numeric columns for statistics
numeric_df = df.select_dtypes(include=['number'])
describe_stats = numeric_df.describe().round(4).to_dict()

# Per-station analysis
stations_count = df['station'].value_counts().to_dict()
station_stats = {}
for station in df['station'].unique():
    station_data = numeric_df[df['station'] == station]
    station_stats[station] = {
        "count": int(len(station_data)),
        "mean_irg": float(station_data['irg'].mean()) if 'irg' in station_data.columns else None,
        "mean_cs_137_emission": float(station_data['cs_137_emission'].mean()) if 'cs_137_emission' in station_data.columns else None,
        "mean_co_60_emission": float(station_data['co_60_ emission'].mean()) if 'co_60_ emission' in station_data.columns else None,
    }

# Per-year analysis
yearly_stats = {}
if 'year' in df.columns:
    for year in sorted(df['year'].unique()):
        year_data = numeric_df[df['year'] == year]
        yearly_stats[str(year)] = {
            "count": int(len(year_data)),
            "mean_cs_137_emission": float(year_data['cs_137_emission'].mean()) if 'cs_137_emission' in year_data.columns else None,
            "mean_co_60_emission": float(year_data['co_60_ emission'].mean()) if 'co_60_ emission' in year_data.columns else None,
            "mean_irg": float(year_data['irg'].mean()) if 'irg' in year_data.columns else None,
        }

# PCA results
pca_info = {
    "n_components": int(pca.n_components_),
    "explained_variance_ratio": [float(x) for x in pca.explained_variance_ratio_],
    "total_variance_explained": float(sum(pca.explained_variance_ratio_)),
}

research_report = {
    "metadata": {
        "module": "data_research",
        "version": "1.0"
    },
    "summary": {
        "total_rows": int(df.shape[0]),
        "total_columns": int(df.shape[1]),
        "stations": list(df['station'].unique()),
        "year_range": [int(df['year'].min()), int(df['year'].max())]
    },
    "descriptive_statistics": describe_stats,
    "station_analysis": station_stats,
    "yearly_analysis": yearly_stats,
    "pca_analysis": pca_info,
    "correlation_analysis": {
        "n_features": int(corr_matr.shape[0]),
        "top_correlations": corr_matr.values.flatten().max() if len(corr_matr) > 0 else None,
    },
    "figures_generated": [
        "data_distributions.png",
        "cs_137_emission_by_year.png",
        "co_60_emission_by_year.png",
        "avg_irg_by_station.png",
        "avg_irg_indx_by_station.png",
        "cs137_dump_vs_volume.png",
        "co60_dump_vs_volume.png",
        "cs137_dump_vs_emission.png",
        "co60_vs_irg_haes.png",
        "pca_2d.png",
        "correlation_matrix.png"
    ]
}

# Save to JSON
with open(RESEARCH_REPORT, 'w', encoding='utf-8') as f:
    json.dump(research_report, f, indent=2, ensure_ascii=False)

print(f"Research report saved to: {RESEARCH_REPORT}")
print(f"\nResearch Summary:")
print(f"  - Total rows: {research_report['summary']['total_rows']}")
print(f"  - Total columns: {research_report['summary']['total_columns']}")
print(f"  - Stations: {research_report['summary']['stations']}")
print(f"  - PCA variance explained: {research_report['pca_analysis']['total_variance_explained']:.2%}")
print(f"  - Figures generated: {len(research_report['figures_generated'])}")

print("\n[data_research] Done.")
