import pandas as pd

df = pd.read_excel('../data/raw/nuclear_safety_q4_2025.xlsx')

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

df.to_csv('../data/raw/clean_data.csv')