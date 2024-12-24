import streamlit as st
import os
import sys

# Add src folder to system path, as it's in a different folder from this file
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

# Import aggregated_scores from random_forest_model.py
from random_forest_model import aggregated_scores

# Import the functions from sentiment analysis file
from ai_sentiment_analysis import main as sentiment_analysis

# Set the page configuration
st.set_page_config(page_title="Manufacturer Analysis", page_icon="📊", layout="wide")

# Page Title
st.title("Manufacturer Analysis")
st.write("Welcome to the Manufacturer Analysis page. Here you can explore sustainability efforts and metrics for different car manufacturers. Use the dropdown menu to select a manufacturer and view their detailed analysis.")

# Dropdown menu for selecting manufacturers
manufacturers = ['BMW', 'Ford', 'General Motors', 'Honda', 'Hyundai', 'Kia', 'Mazda', 'Mercedes', 'Nissan', 'Stellantis', 'Subaru', 'Toyota', 'Volkswagen']
selected_manufacturer = st.selectbox("Select a Manufacturer:", manufacturers)

# Define file paths for respective graphs
forecast_plot_path = f"manufacturer_forecast_plots/{selected_manufacturer}_forecast_plot.png"
co2_plot_path = f"manufacturer_co2_mpg_plots/{selected_manufacturer}_co2_plot.png"
mpg_plot_path = f"manufacturer_co2_mpg_plots/{selected_manufacturer}_mpg_plot.png"
co2_reduction_rate_path = f"manufacturer_advanced_visuals/{selected_manufacturer}_co2_reduction_rate.png"
mpg_growth_rate_path = f"manufacturer_advanced_visuals/{selected_manufacturer}_mpg_growth_rate.png"
co2_to_mpg_ratio_path = f"manufacturer_advanced_visuals/{selected_manufacturer}_co2_to_mpg_ratio.png"

# Display forecast plot with description box
st.subheader(f"Analysis for {selected_manufacturer}")
st.subheader("Sustainability Score Forecast")
col1, col2 = st.columns([2, 0.8])
with col1:
    if os.path.exists(forecast_plot_path):
        st.image(forecast_plot_path, width=1200)
    else:
        st.error(f"Plot not found: {forecast_plot_path}")
with col2:
    st.markdown(
        """
        <div>
            <p style="font-size: 20px; line-height: 2.0;">
                This graph shows the historical and predicted sustainability score trends for the selected manufacturer. 
                The confidence interval highlights the uncertainty in predictions.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Display CO2 plot with description box
st.subheader("Real-World CO2 Emissions Over Time")
col1, col2 = st.columns([2, 0.8])
with col1:
    if os.path.exists(co2_plot_path):
        st.image(co2_plot_path, width=1200)
    else:
        st.error(f"Plot not found: {co2_plot_path}")
with col2:
    st.markdown(
        """
        <div>
            <p style="font-size: 20px; line-height: 2.0;">
                This graph shows the real-world (not under testing conditions) CO2 emissions from the cars of these manufacturers.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Display MPG plot with description box
st.subheader("Real-World MPG Over Time")
col1, col2 = st.columns([2, 0.8])
with col1:
    if os.path.exists(mpg_plot_path):
        st.image(mpg_plot_path, width=1200)
    else:
        st.error(f"Plot not found: {mpg_plot_path}")
with col2:
    st.markdown(
        """
        <div>
            <p style="font-size: 20px; line-height: 2.0;">
                This graph shows the real-world (not under testing conditions) MPG from the cars of these manufacturers. This gives insights into these cars' efficiency, and how many miles they are going per gallon consumed.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

# AI Tool for Online Sentiment Analysis
sustainability_score = aggregated_scores[
    (aggregated_scores["Manufacturer"] == selected_manufacturer) &
    (aggregated_scores["Model Year"] == 2024)
]["Yearly Sustainability Score"].values[0]

st.subheader("AI Sentiment Analysis")
if st.button("Run Sentiment Analysis"):
    pdf_path = f"sustainability_reports/{selected_manufacturer} Sustainability Report.pdf"  # Example path for manufacturer-specific PDFs
    if os.path.exists(pdf_path):
        with st.spinner("Running sentiment analysis. This may take a few moments..."):
            from ai_sentiment_analysis import main as sentiment_analysis
            final_score, explanation = sentiment_analysis(selected_manufacturer, sustainability_score, pdf_path=pdf_path)
            
            st.write(f"Adjusted Sustainability Score: {final_score:.2f}")
            st.write("Explanation:")
            st.write(explanation)
    else:
        st.error(f"PDF not found for {selected_manufacturer}.")
