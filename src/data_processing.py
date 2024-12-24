import pandas as pd
emissions_data = pd.read_csv("data\emissions_data.csv")

# As many manufacturers in the data set don't have valid entries before 2008, to maintain consistency, we will only work with the data from 2008 onwards
emissions_data['Model Year'] = emissions_data['Model Year'].replace('Prelim. 2024', '2024')
emissions_data['Model Year'] = pd.to_numeric(emissions_data['Model Year'])
data_2008 = emissions_data[emissions_data['Model Year'] >= 2008]

# # Separating the data for all the manufacturers combined, and the separate unique manufacturers
specific_manufacturers_data = data_2008[data_2008['Manufacturer'] != 'All']

# Filtering the relevant columns for our analysis
relevant_columns = [
    'Manufacturer', 'Model Year', 'Vehicle Type', 'Production (000)', 
    'Real-World MPG', 'Real-World CO2 (g/mi)', 'Ton-MPG (Real-World)', 'Weight (lbs)',
    'Powertrain - Diesel', 
    'Powertrain - Battery Electric Vehicle (BEV)',
    'Powertrain - Plug-in Hybrid Electric Vehicle (PHEV)',
    'Powertrain - Fuel Cell Electric Vehicle (FCEV)',
    'Powertrain - Other (incl. CNG)',
    'Powertrain - Gasoline Mild Hybrid/MHEV',
    'Powertrain - Gasoline Strong Hybrid/HEV',
    'Powertrain - Gasoline with Start/Stop',
    'Powertrain - Gasoline without Start/Stop'
]

# Filter the dataset for specific manufacturers (excluding "All") and relevant columns
specific_manufacturers_filtered = specific_manufacturers_data[relevant_columns].copy()

if specific_manufacturers_filtered.empty:
    print("No data available for plotting.")
else:
    print("Successfully filtered the data.")