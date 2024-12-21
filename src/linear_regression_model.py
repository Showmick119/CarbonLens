import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import numpy as np
from statsmodels.stats.outliers_influence import variance_inflation_factor
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

# Cleaning the powertrain column's values
for powertrain in powertrain_columns:
    specific_manufacturers_filtered[powertrain] = specific_manufacturers_filtered[powertrain].replace('-',0)
    specific_manufacturers_filtered[powertrain] = specific_manufacturers_filtered[powertrain].astype(str)
    specific_manufacturers_filtered[powertrain] = specific_manufacturers_filtered[powertrain].str.strip('%')
    specific_manufacturers_filtered[powertrain] = specific_manufacturers_filtered[powertrain].astype(float)

specific_manufacturers_filtered[powertrain_columns] = scaler.fit_transform(specific_manufacturers_filtered[powertrain_columns])

# Assign weights to powertrain columns
powertrain_weights = {
    'Powertrain - Diesel': -0.3,  # Strong negative weight due to high emissions
    'Powertrain - Battery Electric Vehicle (BEV)': 0.4,  # Higher positive weight for sustainability
    'Powertrain - Plug-in Hybrid Electric Vehicle (PHEV)': 0.25,  # Transitional technology
    'Powertrain - Fuel Cell Electric Vehicle (FCEV)': 0.35,  # Promising but less prevalent than BEV
    'Powertrain - Other (incl. CNG)': 0.1,  # Moderate weight for cleaner fuel alternative
    'Powertrain - Gasoline Mild Hybrid/MHEV': 0.15,  # Intermediate improvement
    'Powertrain - Gasoline Strong Hybrid/HEV': 0.2,  # Stronger hybrid sustainability
    'Powertrain - Gasoline with Start/Stop': 0.1,  # Small positive impact
    'Powertrain - Gasoline without Start/Stop': -0.15  # Penalize lack of efficiency improvements
}

# Calculate weighted sum for powertrain columns
for col, weight in powertrain_weights.items():
    specific_manufacturers_filtered['Powertrain Contribution'] = sum(specific_manufacturers_filtered[col] * weight)

# Manually combine into Sustainability Score, a baseline with which we can compare the value predicted by the Linear Regression Model
specific_manufacturers_filtered['Sustainability Score'] = (
    specific_manufacturers_filtered['Inverted CO2'] * 0.4 +  # Adjusted weight
    specific_manufacturers_filtered['Ton-MPG (Real-World)'] * 0.3 +
    specific_manufacturers_filtered['Powertrain Contribution'] * 0.3  # Higher weight for powertrain
)

# Define the features (X) and target (y)
y = specific_manufacturers_filtered['Sustainability Score']
features = powertrain_columns + ['Ton-MPG (Real-World)'] + ['Inverted CO2']
X = specific_manufacturers_filtered[features]

# Train a Linear Regression model
model = LinearRegression()
model.fit(X, y)

# Predict sustainability scores
specific_manufacturers_filtered['Predicted Sustainability Score'] = model.predict(X)

# Checking the sustainability scores
print(specific_manufacturers_filtered[['Manufacturer', 'Predicted Sustainability Score']].head())

# Testing whether the linear regression model effectively replicates the manual formula
mse = mean_squared_error(y, specific_manufacturers_filtered['Predicted Sustainability Score'])
print(f"Mean Squared Error: {mse}")

# Normalize predicted scores to [0, 100] with 100 being most sustainable and 0 being least sustainable
specific_manufacturers_filtered['Sustainability Score (Normalized)'] = (
    100 * (specific_manufacturers_filtered['Predicted Sustainability Score'] -
           specific_manufacturers_filtered['Predicted Sustainability Score'].min()) /
           (specific_manufacturers_filtered['Predicted Sustainability Score'].max() -
            specific_manufacturers_filtered['Predicted Sustainability Score'].min())
)

# Check the normalized sustainability scores for the Manufacturers
print(specific_manufacturers_filtered[['Manufacturer', 'Sustainability Score (Normalized)']].head())

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model on training data
model.fit(X_train, y_train)

# Evaluate on testing data
y_pred_test = model.predict(X_test)
mse_test = mean_squared_error(y_test, y_pred_test)
print(f"Test MSE: {mse_test}")

feature_importance = pd.DataFrame({'Feature': features, 'Weight': model.coef_})
print(feature_importance)

vif_data = pd.DataFrame()
vif_data["Feature"] = features
vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
print(vif_data)

# Group by Manufacturer and calculate the mean sustainability score across the years of 2008-2024
aggregated_scores = specific_manufacturers_filtered.groupby('Manufacturer', as_index=False).agg(
    {'Sustainability Score (Normalized)': 'mean'}
)

# Rename the aggregated column for clarity
aggregated_scores.rename(columns={'Sustainability Score (Normalized)': 'Aggregated Sustainability Score'}, inplace=True)

# Check the grouped results
print(aggregated_scores)

# Save the results from the Linear Regression Model to a CSV File
aggregated_scores.to_csv("Linear_Regression_Model_Results.csv")