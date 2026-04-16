import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

plt.style.use('default')

# Load data
df = pd.read_csv('../data/raw/clean_data.csv')

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

