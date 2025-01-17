import pandas as pd
from random_forest_model import aggregated_scores
from prophet import Prophet
from prophet.diagnostics import cross_validation, performance_metrics
import matplotlib.pyplot as plt
import os

# Sorting the aggregated scores by Manufacturer
manufacturers = aggregated_scores['Manufacturer'].unique()

# Creating individual DataFrames for each Manufacturer
manufacturer_data = {
    manufacturer: aggregated_scores[aggregated_scores['Manufacturer'] == manufacturer].reset_index(drop=True)
    for manufacturer in manufacturers
}

# Directory to save the plots
plots_dir = "manufacturer_forecast_plots"
os.makedirs(plots_dir, exist_ok=True)

forecasts = {}

for manufacturer, data in manufacturer_data.items():
    # Apply data smoothing with a rolling mean
    data['Smoothed Sustainability Score'] = (
        data['Yearly Sustainability Score']
        .rolling(window=3, min_periods=1)  # Smooth over a 3-year window
        .mean()
    )

    # Prepare data for the Prophet model
    data = data[['Model Year', 'Smoothed Sustainability Score']]
    data = data.rename(columns={'Model Year': 'ds', 'Smoothed Sustainability Score': 'y'})
    data['ds'] = pd.to_datetime(data['ds'], format='%Y')

    # Initialize and fit the Prophet model
    model = Prophet(
        yearly_seasonality=True, 
        changepoint_prior_scale=0.1, 
        seasonality_prior_scale=0.2
    )
    model.fit(data)

    # Create a DataFrame for future years
    future = model.make_future_dataframe(periods=10, freq='Y')

    # Predict future sustainability scores
    forecast = model.predict(future)

    # Save forecast results
    forecasts[manufacturer] = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

    # Plotting
    fig, ax = plt.subplots(figsize=(12, 5))  # Wider and slightly larger plot
    fig.patch.set_alpha(0)  # Transparent figure background
    ax.set_facecolor('none')  # Transparent axes background

    # Plot observed and forecasted data
    ax.plot(data['ds'], data['y'], 'o', label='Observed Data', color='white')
    ax.plot(forecast['ds'], forecast['yhat'], '-', label='Forecast', color='cyan', linewidth=2)
    ax.fill_between(
        forecast['ds'].dt.to_pydatetime(),
        forecast['yhat_lower'],
        forecast['yhat_upper'],
        color='blue',
        alpha=0.3,
        label='Confidence Interval'
    )

    # Enhance axis labels and ticks
    ax.set_xlabel("Year", fontsize=12, color='white')  # Removed bold styling
    ax.set_ylabel("Sustainability Score", fontsize=12, color='white')  # Removed bold styling
    ax.tick_params(axis='x', colors='white', labelsize=10)
    ax.tick_params(axis='y', colors='white', labelsize=10)

    # Add grid lines
    ax.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.7)

    # Add legend with a smaller label box
    ax.legend(
        loc='upper left', fontsize=10, facecolor='black', edgecolor='white', labelspacing=0.4, labelcolor='white'
    )

    # Adjust layout to reduce empty space
    plt.tight_layout()

    # Save the plot
    fig.savefig(f"{plots_dir}/{manufacturer}_forecast_plot.png", dpi=300, transparent=True, bbox_inches='tight')  # Minimized space
    plt.close(fig)

    print(f"Saved plot for {manufacturer} to {plots_dir}/{manufacturer}_forecast_plot.png")


# # Cross-validation
# df_cv = cross_validation(model, initial='730 days', period='180 days', horizon='365 days')

# # Evaluate performance and check if we are getting low values for rmse and mape
# df_p = performance_metrics(df_cv)
# print(df_p[['horizon', 'rmse', 'mape']])