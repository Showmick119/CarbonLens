import pandas as pd
from random_forest_model import aggregated_scores
from prophet import Prophet
import matplotlib.pyplot as plt
import os

# Sorting the aggregated scores by the specific Manufacturer
manufacturers = aggregated_scores['Manufacturer'].unique()

# Creating individual DataFrames for the individual Manufacturer data
manufacturer_data = {
    manufacturer: aggregated_scores[aggregated_scores['Manufacturer'] == manufacturer].reset_index(drop=True)
    for manufacturer in manufacturers
}

# Making the directory where the plots will be saved
plots_dir = "manufacturer_forecast_plots"
os.makedirs(plots_dir, exist_ok=True)

forecasts = {}

for manufacturer, data in manufacturer_data.items():
    # Prepare data for the Prophet time-series model
    data = data[['Model Year', 'Yearly Sustainability Score']]
    data = data.rename(columns={'Model Year': 'ds', 'Yearly Sustainability Score': 'y'})
    data['ds'] = pd.to_datetime(data['ds'], format='%Y')

    # Initializing and fitting the Prophet model for time-series analysis
    model = Prophet()
    model.fit(data)

    # Creating DataFrame for future years
    future = model.make_future_dataframe(periods=10, freq='Y')
    
    # Predicting future sustainability scores based on the historical trends
    forecast = model.predict(future)

    # Save forecast results
    forecasts[manufacturer] = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

    # Generating the plot
    fig = model.plot(forecast)

    # Adding x and y-axis labels
    ax = fig.gca()
    ax.set_xlabel("Year")
    ax.set_ylabel("Sustainability Score")

    # Saving the plot as a file
    fig.savefig(f"{plots_dir}/{manufacturer}_forecast_plot.png")
    plt.close(fig)

    # Message to indicate successful execution of the code
    print(f"Saved plot for {manufacturer} to {plots_dir}/{manufacturer}_forecast_plot.png")