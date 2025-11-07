import pandas as pd

# Read the metadata to identify actual countries
metadata = pd.read_csv('Metadata_Country_API_NY.GDP.MKTP.CD_DS2_en_csv_v2_130122.csv')

# Filter out aggregates and regions (they have empty Region field)
# Keep only rows with a non-empty Region (actual countries)
actual_countries = metadata[metadata['Region'].notna() & (metadata['Region'] != '')]
country_codes = actual_countries['Country Code'].tolist()

print(f"Found {len(country_codes)} actual countries")

# Read the GDP data (skip first 4 rows which are metadata)
gdp_data = pd.read_csv('API_NY.GDP.MKTP.CD_DS2_en_csv_v2_130122.csv', skiprows=4)

# Filter for actual countries only
gdp_cleaned = gdp_data[gdp_data['Country Code'].isin(country_codes)]

print(f"Filtered GDP data to {len(gdp_cleaned)} countries")

# Convert from wide format (years as columns) to long format
# Get year columns (1960-2024)
year_columns = [col for col in gdp_cleaned.columns if col.isdigit()]

# Melt the dataframe
gdp_long = pd.melt(
    gdp_cleaned,
    id_vars=['Country Name', 'Country Code'],
    value_vars=year_columns,
    var_name='Year',
    value_name='GDP'
)

# Remove rows with missing GDP values
gdp_long = gdp_long.dropna(subset=['GDP'])

# Convert Year to integer
gdp_long['Year'] = gdp_long['Year'].astype(int)

# Sort by country and year
gdp_long = gdp_long.sort_values(['Country Code', 'Year'])

# Save to new CSV
gdp_long.to_csv('gdp_cleaned.csv', index=False)

print(f"\n✅ Saved cleaned data to gdp_cleaned.csv")
print(f"Total records: {len(gdp_long)}")
print(f"Year range: {gdp_long['Year'].min()} - {gdp_long['Year'].max()}")
print(f"\nSample countries:")
print(gdp_long[gdp_long['Country Code'].isin(['USA', 'CHN', 'DEU', 'JPN', 'IND'])].groupby('Country Code')['Year'].agg(['min', 'max']))
