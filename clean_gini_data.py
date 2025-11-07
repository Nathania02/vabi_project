import pandas as pd
import os

# Read metadata to identify actual countries
metadata = pd.read_csv('GINI DATA/Metadata_Country_API_SI.POV.GINI_DS2_en_csv_v2_134799.csv')

# Filter to actual countries (those with a Region)
actual_countries = metadata[metadata['Region'].notna() & (metadata['Region'] != '')]
country_codes = actual_countries['Country Code'].tolist()

print(f"Found {len(country_codes)} actual countries")

# Read GINI data (skip first 4 rows which are metadata)
gini_data = pd.read_csv('GINI DATA/API_SI.POV.GINI_DS2_en_csv_v2_134799.csv', skiprows=4)

# Filter to actual countries only
gini_cleaned = gini_data[gini_data['Country Code'].isin(country_codes)]
print(f"Filtered GINI data to {len(gini_cleaned)} countries")

# Get year columns (all columns that are numeric years)
year_columns = [col for col in gini_cleaned.columns if col.isdigit()]

# Transform from wide to long format
gini_long = pd.melt(
    gini_cleaned,
    id_vars=['Country Name', 'Country Code'],
    value_vars=year_columns,
    var_name='Year',
    value_name='GINI'
)

# Convert Year to integer and GINI to float
gini_long['Year'] = gini_long['Year'].astype(int)
gini_long['GINI'] = pd.to_numeric(gini_long['GINI'], errors='coerce')

# Remove rows with null GINI values
gini_long = gini_long.dropna(subset=['GINI'])

# Sort by country and year
gini_long = gini_long.sort_values(['Country Code', 'Year'])

# Save cleaned data
gini_long.to_csv('gini_cleaned.csv', index=False)

print(f"\n✅ Saved cleaned data to gini_cleaned.csv")
print(f"Total records: {len(gini_long)}")
print(f"Year range: {gini_long['Year'].min()} - {gini_long['Year'].max()}")
print(f"\nSample countries with year coverage:")
print(gini_long.groupby('Country Code')['Year'].agg(['min', 'max']).head(10))
