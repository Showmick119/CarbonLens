import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
import numpy as np
from data_processing import specific_manufacturers_filtered

# # Load the dataset
# file_path = "data\emissions_data.csv" # Ensure the file is in the same directory
# emissions_data = pd.read_csv(file_path)

# Step 1: Normalize Relevant Numerical Columns
columns_to_normalize = ['Real-World CO2 (g/mi)', 'Ton-MPG (Real-World)']
specific_manufacturers_filtered[columns_to_normalize] = specific_manufacturers_filtered[columns_to_normalize].replace('-', None).astype(float)
specific_manufacturers_filtered[columns_to_normalize] = specific_manufacturers_filtered[columns_to_normalize].fillna(specific_manufacturers_filtered[columns_to_normalize].mean())
scaler = MinMaxScaler()
specific_manufacturers_filtered[columns_to_normalize] = scaler.fit_transform(specific_manufacturers_filtered[columns_to_normalize])
print("Success")
print(specific_manufacturers_filtered.loc[:,["Powertrain - Diesel", "Ton-MPG (Real-World)"]])

# Define powertrain columns and weights
powertrain_columns = [
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

'''Progress:
Currently we are encoding and standardizing the powertrain column. We will do the same for a few other columns and then feed this standardized data into a Linear
Regression model to give sustainability scores to each company. And to also predict future sustainability. And then we will web scrape into the companies manufacturing
processes. And use AI models to give them suggestions on how to improve. We will also use the csv file data to give these recommendations. Additionally, we will 
implement an AI tool for consumers, where they can upload descriptions or images of cars and we will use web scraping and AI to analyze the sustainability of the car.'''

for powertrain in powertrain_columns:
    specific_manufacturers_filtered[powertrain] = specific_manufacturers_filtered[powertrain].replace('-',0)
    
    # specific_manufacturers_filtered[powertrain] = specific_manufacturers_filtered[powertrain].apply(lambda x: x.strip('%') if type(x) == 'str' else x)
    # specific_manufacturers_filtered[powertrain] = specific_manufacturers_filtered[powertrain].astype('float64')
    # specific_manufacturers_filtered[powertrain] = specific_manufacturers_filtered[powertrain].fillna(0)


print(specific_manufacturers_filtered['Powertrain - Battery Electric Vehicle (BEV)'])

# specific_manufacturers_filtered[powertrain_columns] = (
#     specific_manufacturers_filtered[powertrain_columns]
#     .replace('-', 0)  # Replace '-' with 0
#     .apply(lambda x: x.str.rstrip('%') if x.dtype == 'object' else x)  # Remove % symbol
#     .astype(float)  # Convert to numeric
#     .fillna(0)  # Fill NaN with 0
# )

# for item in powertrain_columns:
#     if specific_manufacturers_filtered[item].empty:
#         print(item)

# specific_manufacturers_filtered[powertrain_columns] = (
#     specific_manufacturers_filtered[powertrain_columns]
#     .replace('-', 0)
#     .apply(pd.to_numeric, errors='coerce')
#     .fillna(0)
# )

# # Step 2: Convert percentages to decimals if necessary
# specific_manufacturers_filtered[powertrain_columns] = (
#     specific_manufacturers_filtered[powertrain_columns] / 100
# )

# print(specific_manufacturers_filtered['Powertrain - Diesel'])

# powertrain_weights = {
#     'Powertrain - Diesel': 5,
#     'Powertrain - Battery Electric Vehicle (BEV)': 100,
#     'Powertrain - Plug-in Hybrid Electric Vehicle (PHEV)': 75,
#     'Powertrain - Fuel Cell Electric Vehicle (FCEV)': 90,
#     'Powertrain - Other (incl. CNG)': 10,
#     'Powertrain - Gasoline Mild Hybrid/MHEV': 60,
#     'Powertrain - Gasoline Strong Hybrid/HEV': 50,
#     'Powertrain - Gasoline with Start/Stop': 40,
#     'Powertrain - Gasoline without Start/Stop': 10
# }

# # Create an encoded powertrain column
# def calculate_powertrain_score(row):
#     scores = [row[col] * powertrain_weights[col] for col in powertrain_columns if col in row and pd.notna(row[col])]
#     return max(scores) if scores else 0

# specific_manufacturers_filtered['Powertrain_Encoded'] = specific_manufacturers_filtered.apply(calculate_powertrain_score, axis=1)
# specific_manufacturers_filtered['Real-World CO2 (g/mi)'] = pd.to_numeric(specific_manufacturers_filtered['Real-World CO2 (g/mi)'], errors='coerce')
# specific_manufacturers_filtered['Ton-MPG (Real-World)'] = pd.to_numeric(specific_manufacturers_filtered['Ton-MPG (Real-World)'], errors='coerce')
# specific_manufacturers_filtered.to_csv("sample.csv")
# print("Success")

# # Select features for clustering
# features = emissions_data[[
#     'Real-World CO2 (g/mi)', 'Ton-MPG (Real-World)', 'Powertrain_Encoded'
# ]].copy()

# # Normalize features for clustering
# features_normalized = scaler.fit_transform(features)

# # Apply K-Means clustering
# n_clusters = 5  # Define the number of clusters
# kmeans = KMeans(n_clusters=n_clusters, random_state=42)
# emissions_data['Sustainability_Cluster'] = kmeans.fit_predict(features_normalized)

# # Map clusters to sustainability ratings
# # Define ratings for each cluster (adjust based on domain knowledge)
# cluster_to_rating = {
#     0: 90,  # Example: Cluster 0 is most sustainable
#     1: 70,
#     2: 50,
#     3: 30,
#     4: 10   # Example: Cluster 4 is least sustainable
# }

# emissions_data['Sustainability_Rating'] = emissions_data['Sustainability_Cluster'].map(cluster_to_rating)

# # Save the updated dataset
# output_path = "sustainability_ratings.csv"
# emissions_data.to_csv(output_path, index=False)

# print(f"Sustainability ratings have been saved to {output_path}.")
