import pandas as pd

# Read the World Bank poverty headcount data (skip first 4 metadata rows)
df = pd.read_csv('Headcount/API_SI.POV.DDAY_DS2_en_csv_v2_128451.csv', skiprows=4)

# Read metadata to filter only actual countries
metadata = pd.read_csv('Headcount/Metadata_Country_API_SI.POV.DDAY_DS2_en_csv_v2_128451.csv')

# Filter to only actual countries (those with a Region assigned)
actual_countries = metadata[metadata['Region'].notna()]['Country Code'].tolist()
print(f"Found {len(actual_countries)} actual countries in metadata")

# Filter main data to only these countries
df_filtered = df[df['Country Code'].isin(actual_countries)].copy()
print(f"Filtered to {len(df_filtered)} country rows")

# Get year columns (1960-2024)
year_columns = [str(year) for year in range(1960, 2025)]

# Melt the dataframe to long format
df_long = df_filtered.melt(
    id_vars=['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code'],
    value_vars=year_columns,
    var_name='Year',
    value_name='Headcount'
)

# Drop rows with missing headcount values
df_long = df_long.dropna(subset=['Headcount'])

# Convert Year to integer and Headcount to float
df_long['Year'] = df_long['Year'].astype(int)
df_long['Headcount'] = df_long['Headcount'].astype(float)

# Keep only needed columns
df_clean = df_long[['Country Name', 'Country Code', 'Year', 'Headcount']].copy()

# Sort by Country Code and Year
df_clean = df_clean.sort_values(['Country Code', 'Year']).reset_index(drop=True)

# Save to CSV
df_clean.to_csv('headcount_cleaned.csv', index=False)

print(f"\n✅ Cleaned data saved to headcount_cleaned.csv")
print(f"Total records: {len(df_clean):,}")
print(f"Countries: {df_clean['Country Code'].nunique()}")
print(f"Year range: {df_clean['Year'].min()}-{df_clean['Year'].max()}")

# Show coverage statistics
print("\n📊 Data Coverage by Year (recent years):")
coverage = df_clean.groupby('Year').size().sort_index(ascending=False)
print(coverage.head(20))

# Check Top 5 countries
print("\n🏆 Top 5 Economies Coverage:")
top5 = ['USA', 'CHN', 'DEU', 'JPN', 'IND']
df_top5 = df_clean[df_clean['Country Code'].isin(top5)]
print(df_top5.groupby('Year').agg({'Country Code': lambda x: list(x.unique())}).tail(20))
