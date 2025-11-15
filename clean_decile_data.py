import pandas as pd

# Read the CSV
df = pd.read_csv('Decile/povertyinequality.csv')

# Filter for United States data only
us_data = df[df['country_name'] == 'United States'].copy()

# Check what columns we have and what years
print("Available columns:", us_data.columns.tolist())
print("\nUS data shape:", us_data.shape)
print("\nYears available:", sorted(us_data['reporting_year'].unique()))

# Select relevant columns for decile analysis
decile_cols = ['decile1', 'decile2', 'decile3', 'decile4', 'decile5', 
               'decile6', 'decile7', 'decile8', 'decile9', 'decile10']
us_decile = us_data[['country_name', 'reporting_year', 'welfare_type'] + decile_cols].copy()

# Sort by year
us_decile = us_decile.sort_values('reporting_year')

# Save cleaned data
us_decile.to_csv('us_decile_cleaned.csv', index=False)

print("\n--- Cleaned US Decile Data ---")
print(us_decile)

# Show the most recent year data
if len(us_decile) > 0:
    latest = us_decile.iloc[-1]
    print("\n--- Most Recent Year Data ---")
    print(f"Year: {latest['reporting_year']}")
    print(f"Welfare Type: {latest['welfare_type']}")
    print("\nDecile Distribution:")
    for i in range(1, 11):
        decile_val = latest[f'decile{i}'] * 100  # Convert to percentage
        print(f"Decile {i}: {decile_val:.2f}%")
