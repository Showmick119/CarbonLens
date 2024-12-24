import pandas as pd
import numpy as np
from data_processing import specific_manufacturers_filtered
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import make_scorer, mean_squared_error
from sklearn.model_selection import cross_val_score

# Normalize Relevant Numerical Columns
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

# Manually combine into Sustainability Score, a benchmark with which we can train the Random Forest Model and evaluate the values it predicts
specific_manufacturers_filtered['Sustainability Score'] = (
    specific_manufacturers_filtered['Inverted CO2'] * 0.4 +  # Adjusted weight
    specific_manufacturers_filtered['Ton-MPG (Real-World)'] * 0.3 +
    specific_manufacturers_filtered['Powertrain Contribution'] * 0.3  # Higher weight for powertrain
)

# Combine features and target
features = powertrain_columns + ['Ton-MPG (Real-World)', 'Inverted CO2']
X = specific_manufacturers_filtered[features]
y = specific_manufacturers_filtered['Sustainability Score']

# Split data into training and testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest Model
random_forest = RandomForestRegressor(n_estimators=100, random_state=42)
random_forest.fit(X_train, y_train)

# Evaluate the Model
y_pred_test = random_forest.predict(X_test)
mse_test = mean_squared_error(y_test, y_pred_test)
print(f"Random Forest Test MSE: {mse_test}")

# Predict Sustainability Scores for All Data
specific_manufacturers_filtered['Predicted Sustainability Score'] = random_forest.predict(X)

# Normalize scores to [0, 100]
specific_manufacturers_filtered['Sustainability Score (Normalized)'] = (
    100 * (specific_manufacturers_filtered['Predicted Sustainability Score'] - 
           specific_manufacturers_filtered['Predicted Sustainability Score'].min()) / 
           (specific_manufacturers_filtered['Predicted Sustainability Score'].max() - 
            specific_manufacturers_filtered['Predicted Sustainability Score'].min())
)

# Group by Manufacturer and Model Year to retain scores for each year
aggregated_scores = specific_manufacturers_filtered.groupby(
    ['Manufacturer', 'Model Year'], as_index=False
).agg({'Sustainability Score (Normalized)': 'mean'})

# Rename the column to make it more descriptive
aggregated_scores.rename(columns={'Sustainability Score (Normalized)': 'Yearly Sustainability Score'}, inplace=True)

# # Save results to a CSV file
# aggregated_scores.to_csv("random_forest_model_results.csv", index=False)
# print("Random Forest Model results saved to random_forest_model_results.csv")


# '''Testing the Model's Accuracy as well as measuring how each feature/metric contributes to the Sustainability Score for the Manufacturer in that given year'''
# # Define a custom scorer for MSE
# mse_scorer = make_scorer(mean_squared_error, greater_is_better=False)

# # Perform k-fold cross-validation
# k = 5  # Number of folds
# cv_scores = cross_val_score(random_forest, X, y, cv=k, scoring=mse_scorer)

# # Convert negative MSE to positive
# cv_scores = -cv_scores

# print(f"Cross-Validation MSE scores for each fold: {cv_scores}")
# print(f"Average Cross-Validation MSE: {np.mean(cv_scores)}")

# # Get feature importances from the Random Forest model
# feature_importances = random_forest.feature_importances_

# # Create a DataFrame to visualize the feature importance
# features_df = pd.DataFrame({
#     'Feature': features,  # Replace with the feature names used in your model
#     'Importance': feature_importances
# })

# # Sort features by importance
# features_df = features_df.sort_values(by='Importance', ascending=False)

# # Display the feature importance
# print(features_df)