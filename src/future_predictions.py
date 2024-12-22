import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import MinMaxScaler
from data_processing import specific_manufacturers_filtered  # Assuming preprocessing is here
from sklearn.model_selection import train_test_split
import numpy as np

# Define the features (X) and target (y)
features = [
    'Powertrain - Diesel',
    'Powertrain - Battery Electric Vehicle (BEV)',
    'Powertrain - Plug-in Hybrid Electric Vehicle (PHEV)',
    'Powertrain - Fuel Cell Electric Vehicle (FCEV)',
    'Powertrain - Other (incl. CNG)',
    'Powertrain - Gasoline Mild Hybrid/MHEV',
    'Powertrain - Gasoline Strong Hybrid/HEV',
    'Powertrain - Gasoline with Start/Stop',
    'Powertrain - Gasoline without Start/Stop',
    'Inverted CO2',
    'Ton-MPG (Real-World)'
]

X = specific_manufacturers_filtered[features]
y = specific_manufacturers_filtered['Aggregated Sustainability Score']

# Train-test split (for evaluation, if needed)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Load the Random Forest model trained earlier (if serialized, load it here)
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Define percentage improvements for each feature
projection_changes = {
    'Inverted CO2': 0.1,  # 10% improvement
    'Ton-MPG (Real-World)': 0.05,  # 5% improvement
    'Powertrain - Diesel': 0.0,  # Assume no change
    'Powertrain - Battery Electric Vehicle (BEV)': 0.1,  # 10% improvement
    'Powertrain - Plug-in Hybrid Electric Vehicle (PHEV)': 0.08,
    'Powertrain - Fuel Cell Electric Vehicle (FCEV)': 0.1,
    'Powertrain - Other (incl. CNG)': -0.05,  # Assume slight decrease
    'Powertrain - Gasoline Mild Hybrid/MHEV': 0.05,
    'Powertrain - Gasoline Strong Hybrid/HEV': 0.05,
    'Powertrain - Gasoline with Start/Stop': 0.02,
    'Powertrain - Gasoline without Start/Stop': -0.05
}

# Create future features
future_features = X.copy()  # Start with the current features

for feature, change in projection_changes.items():
    if feature in future_features:
        # Apply percentage change
        future_features[feature] = future_features[feature] * (1 + change)

# Predict future sustainability scores
future_predictions = model.predict(future_features)

# Combine results into a DataFrame for easier interpretation
future_results = pd.DataFrame({
    'Manufacturer': specific_manufacturers_filtered['Manufacturer'],  # Assuming this column exists
    'Future Sustainability Score': future_predictions
})

# Group by Manufacturer to calculate average future sustainability score
aggregated_future_results = future_results.groupby('Manufacturer', as_index=False).mean()

# Display the results
print("Projected Future Sustainability Scores:")
print(aggregated_future_results)