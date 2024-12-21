import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import numpy as np
from data_processing import specific_manufacturers_filtered

# Step 1: Normalize Relevant Numerical Columns
columns_to_normalize = ['Real-World CO2 (g/mi)', 'Ton-MPG (Real-World)']
specific_manufacturers_filtered[columns_to_normalize] = specific_manufacturers_filtered[columns_to_normalize].replace('-', None).astype(float)
specific_manufacturers_filtered[columns_to_normalize] = specific_manufacturers_filtered[columns_to_normalize].fillna(specific_manufacturers_filtered[columns_to_normalize].mean())
scaler = MinMaxScaler()
specific_manufacturers_filtered[columns_to_normalize] = scaler.fit_transform(specific_manufacturers_filtered[columns_to_normalize])

# Invert CO2 to align higher values with better sustainability
specific_manufacturers_filtered['Inverted CO2'] = 1 - specific_manufacturers_filtered['Real-World CO2 (g/mi)']

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

for powertrain in powertrain_columns:
    specific_manufacturers_filtered[powertrain] = specific_manufacturers_filtered[powertrain].replace('-',0)
    specific_manufacturers_filtered[powertrain] = specific_manufacturers_filtered[powertrain].astype(str)
    specific_manufacturers_filtered[powertrain] = specific_manufacturers_filtered[powertrain].str.strip('%')
    specific_manufacturers_filtered[powertrain] = specific_manufacturers_filtered[powertrain].astype(float)

specific_manufacturers_filtered[powertrain_columns] = scaler.fit_transform(specific_manufacturers_filtered[powertrain_columns])

# Assign weights to powertrain columns
powertrain_weights = {
    'Powertrain - Diesel': -0.2,  # Negative weight for less sustainable powertrain
    'Powertrain - Battery Electric Vehicle (BEV)': 0.3,
    'Powertrain - Plug-in Hybrid Electric Vehicle (PHEV)': 0.2,
    'Powertrain - Fuel Cell Electric Vehicle (FCEV)': 0.3,
    'Powertrain - Other (incl. CNG)': 0.1,
    'Powertrain - Gasoline Mild Hybrid/MHEV': 0.1,
    'Powertrain - Gasoline Strong Hybrid/HEV': 0.15,
    'Powertrain - Gasoline with Start/Stop': 0.05,
    'Powertrain - Gasoline without Start/Stop': -0.1  # Penalize lack of start/stop tech
}

# Calculate weighted sum for powertrain columns
for col, weight in powertrain_weights.items():
    specific_manufacturers_filtered['Powertrain Contribution'] = sum(specific_manufacturers_filtered[col] * weight)

# Combine into Sustainability Score
specific_manufacturers_filtered['Sustainability Score'] = (
    specific_manufacturers_filtered['Inverted CO2'] * 0.4 +  # Adjusted weight
    specific_manufacturers_filtered['Ton-MPG (Real-World)'] * 0.3 +
    specific_manufacturers_filtered['Powertrain Contribution'] * 0.3  # Higher weight for powertrain
)

# Define the features (X) and target (y)
y = specific_manufacturers_filtered['Sustainability Score']
features = powertrain_columns + columns_to_normalize
X = specific_manufacturers_filtered[features]

# Train a Linear Regression model
model = LinearRegression()
model.fit(X, y)

# Predict sustainability scores
specific_manufacturers_filtered['Predicted Sustainability Score'] = model.predict(X)

# Checking the sustainability scores
print(specific_manufacturers_filtered[['Manufacturer', 'Predicted Sustainability Score']].head())

mse = mean_squared_error(y, specific_manufacturers_filtered['Predicted Sustainability Score'])
print(f"Mean Squared Error: {mse}")


# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model on training data
model.fit(X_train, y_train)

# Evaluate on testing data
y_pred_test = model.predict(X_test)
mse_test = mean_squared_error(y_test, y_pred_test)
print(f"Test MSE: {mse_test}")