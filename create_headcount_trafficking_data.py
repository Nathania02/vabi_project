import pandas as pd

# Load trafficking data
trafficking_df = pd.read_csv('CTDC_global_synthetic_data_v2025_v2.csv')

# Load headcount data
headcount_df = pd.read_csv('headcount_cleaned.csv')

# Filter for organ removal cases and aggregate by country and year
organ_trafficking = trafficking_df[trafficking_df['typeOfExploitationOrganRemoval'] == 1].copy()

# Count organ trafficking cases by country and year
organ_counts = organ_trafficking.groupby(['CountryOfExploitation', 'yearOfRegistration']).size().reset_index(name='OrganCases')

# Rename columns to match headcount data
organ_counts.rename(columns={
    'CountryOfExploitation': 'Country Code',
    'yearOfRegistration': 'Year'
}, inplace=True)

# Merge with headcount data
merged = pd.merge(
    headcount_df,
    organ_counts,
    on=['Country Code', 'Year'],
    how='inner'  # Only keep countries/years with both headcount and trafficking data
)

# Filter out rows with missing data
merged = merged.dropna()

# Sort by year and country
merged = merged.sort_values(['Year', 'Country Name'])

print(f"Combined dataset created:")
print(f"  Total records: {len(merged)}")
print(f"  Countries: {merged['Country Code'].nunique()}")
print(f"  Year range: {merged['Year'].min()}-{merged['Year'].max()}")
print(f"\nSample data:")
print(merged.head(10))
print(f"\nOrgan cases range: {merged['OrganCases'].min()}-{merged['OrganCases'].max()}")
print(f"Headcount range: {merged['Headcount'].min():.2f}-{merged['Headcount'].max():.2f}%")

# Save to CSV
merged.to_csv('headcount_trafficking_combined.csv', index=False)
print("\n✅ Saved to headcount_trafficking_combined.csv")
