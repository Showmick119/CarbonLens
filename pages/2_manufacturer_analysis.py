# Manufacturer Analysis Page
import streamlit as st
import os

# Set the page configuration
st.set_page_config(page_title="Manufacturer Analysis", layout="wide")

# Page Title
st.title("Manufacturer Analysis")
st.write("Welcome to the Manufacturer Analysis page. Here you can explore sustainability efforts and metrics for different car manufacturers. Use the dropdown menu to select a manufacturer and view their detailed analysis.")

# Dropdown menu for selecting manufacturers
manufacturers = ['BMW', 'Ford', 'GM', 'Honda', 'Hyundai', 'Kia', 'Mazda', 'Mercedes', 'Nissan', 'Stellantis', 'Subaru', 'Toyota', 'VW']
selected_manufacturer = st.selectbox("Select a Manufacturer:", manufacturers)

# Define file paths for respective graphs
forecast_plot_path = f"data/manufacturer_forecast_plots/{selected_manufacturer}_forecast_plot.png"
co2_plot_path = f"data/manufacturer_co2_mpg_plots/{selected_manufacturer}_co2_plot.png"
mpg_plot_path = f"data/manufacturer_co2_mpg_plots/{selected_manufacturer}_mpg_plot.png"
advanced_visual_path = f"data/manufacturer_advanced_visuals/{selected_manufacturer}_co2_reduction_rate.png"

# Display forecast plot
st.subheader(f"Analysis for {selected_manufacturer}")
st.subheader("Sustainability Score Forecast")
st.write("This graph shows the historical and predicted sustainability score trends for the selected manufacturer. The confidence interval highlights the uncertainty in predictions.")
if os.path.exists(forecast_plot_path):
    st.image(forecast_plot_path, use_column_width=True)
else:
    st.error(f"Plot not found: {forecast_plot_path}")

# Display CO2 plot
st.subheader("CO2 Reduction Rate Over Time")
st.write("This graph illustrates the percentage change in CO2 reduction over the years. Negative values indicate a rise in CO2 emissions.")
if os.path.exists(co2_plot_path):
    st.image(co2_plot_path, use_column_width=True)
else:
    st.error(f"Plot not found: {co2_plot_path}")

# Display MPG plot
st.subheader("Real-World MPG Over Time")
st.write("This graph shows the Real-World MPG changes over time for the selected manufacturer.")
if os.path.exists(mpg_plot_path):
    st.image(mpg_plot_path, use_column_width=True)
else:
    st.error(f"Plot not found: {mpg_plot_path}")

# Display advanced visualization
st.subheader("Comparative Sustainability Insights")
st.write(f"Here are advanced visualizations highlighting {selected_manufacturer}'s sustainability metrics relative to other manufacturers.")
if os.path.exists(advanced_visual_path):
    st.image(advanced_visual_path, use_column_width=True)
else:
    st.error(f"Plot not found: {advanced_visual_path}")