import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import seaborn as sns

plt.style.use('default')

# Load data
df = pd.read_csv('../data/raw/clean_data.csv')

# Basic checks
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
plt.savefig('reports/lab1/figures/data_distributions.png')
plt.close()

# Avg cs-137 emission by year
avg_cs137 = df.groupby('year')['cs_137_emission'].mean()
plt.figure()
plt.plot(avg_cs137)
plt.title('Average cs_137_emission by year')
plt.savefig('reports/lab1/figures/cs_137_emission_by_year.png')
plt.close()

# Avg co-60 emission by year
avg_co60 = df.groupby('year')['co_60_ emission'].mean()
plt.figure()
plt.plot(avg_co60)
plt.title('Average co_60_emission by year')
plt.savefig('reports/lab1/figures/co_60_emission_by_year.png')
plt.close()

# IRG by station
station_irg = df.groupby('station')['irg'].mean()
stations = df['station'].unique()

plt.figure()
plt.bar(stations, station_irg)
plt.savefig('reports/lab1/figures/avg_irg_by_station.png')
plt.close()

# IRG index by station
station_irg_indx = df.groupby('station')['irg_index'].mean()

plt.figure()
plt.bar(stations, station_irg_indx)
plt.savefig('reports/lab1/figures/avg_irg_indx_by_station.png')
plt.close()

# Scatter plots
plt.figure()
plt.scatter(df['cs_137_dump'], df['volume'])
plt.title('cs_137_dump vs volume')
plt.savefig('reports/lab1/figures/cs137_dump_vs_volume.png')
plt.close()

plt.figure()
plt.scatter(df['co_60_dump'], df['volume'])
plt.title('co_60_dump vs volume')
plt.savefig('reports/lab1/figures/co60_dump_vs_volume.png')
plt.close()

plt.figure()
plt.scatter(df['cs_137_dump'], df['cs_137_emission'])
plt.title('cs_137_dump vs cs_137_emission')
plt.savefig('reports/lab1/figures/cs137_dump_vs_emission.png')
plt.close()

# Filtered scatter (specific station)
mask = df['station'] == 'ХАЕС'

plt.figure()
plt.scatter(df.loc[mask, 'co_60_ emission'], df.loc[mask, 'irg'])
plt.title('co_60_emission vs irg (ХАЕС only)')
plt.savefig('reports/lab1/figures/co60_vs_irg_haes.png')
plt.close()

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
plt.savefig('reports/lab1/figures/pca_2d.png')
plt.close()

# Correlation heatmap
df_corr = df.drop(['station'], axis=1)
corr_matr = df_corr.corr()

plt.figure(figsize=(20, 10))
sns.heatmap(corr_matr, annot=True, cmap='coolwarm', fmt=".2f", square=True)
plt.title('Correlation Matrix Heatmap')
plt.tight_layout()
plt.savefig('reports/lab1/figures/correlation_matrix.png')
plt.close()
