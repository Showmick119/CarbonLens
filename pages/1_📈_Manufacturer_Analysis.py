import streamlit as st
import pandas as pd
import os
import sys

# Load the CSV file containing graph explanations
csv_path = "data/explanations.csv" 
explanations_df = pd.read_csv(csv_path)

# Function to get the explanations for each manufacturer's plots
def get_explanation(manufacturer, graph_type):
    """Fetch explanation for a given manufacturer and graph type from the DataFrame."""
    row = explanations_df[(explanations_df['Manufacturer'] == manufacturer) & 
                          (explanations_df['Graph Type'] == graph_type)]
    if not row.empty:
        return row['Explanation'].values[0]
    else:
        return "Explanation not found for this graph."

# Add src folder to system path, as it's in a different folder from this file
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

# Import aggregated_scores from random_forest_model.py
from random_forest_model import aggregated_scores
from ai_sentiment_analysis import update_cache_metadata

# Set the page configuration
st.set_page_config(page_title="Manufacturer Analysis", page_icon="📈", layout="wide")

# Page Title
st.title("🔎 Manufacturer Analysis")
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
powertrain_pie_chart_path = f"manufacturer_advanced_visuals/{selected_manufacturer}_powertrain_pie_chart.png"

# Header for the analysis of each selected manufacturer
st.subheader(f"Analysis for {selected_manufacturer}")

# Display forecast plot with description box
st.subheader("Sustainability Score Forecast")
col1, col2 = st.columns([2, 0.8])
with col1:
    if os.path.exists(forecast_plot_path):
        st.image(forecast_plot_path, width=1200)
    else:
        st.error(f"Plot not found: {forecast_plot_path}")
with col2:
    explanation = get_explanation(selected_manufacturer, "Sustainability Score")
    st.markdown(
        f"""
        <div>
            <p style="font-size: 15px; line-height: 2.0;">
                {explanation}
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
    explanation = get_explanation(selected_manufacturer, "CO2")
    st.markdown(
        f"""
        <div>
            <p style="font-size: 15px; line-height: 2.0;">
                {explanation}
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
    explanation = get_explanation(selected_manufacturer, "MPG")
    st.markdown(
        f"""
        <div>
            <p style="font-size: 15px; line-height: 2.0;">
                {explanation}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Display CO2 reduction rate plot with description box
st.subheader("CO2 Reduction Rate Over Time")
col1, col2 = st.columns([2, 0.8])
with col1:
    if os.path.exists(co2_reduction_rate_path):
        st.image(co2_reduction_rate_path, width=1200)
    else:
        st.error(f"Plot not found: {co2_reduction_rate_path}")
with col2:
    explanation = get_explanation(selected_manufacturer, "CO2 Reduction")
    st.markdown(
        f"""
        <div>
            <p style="font-size: 15px; line-height: 2.0;">
                {explanation}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Display MPG growth rate plot with description box
st.subheader("MPG Growth Rate Over Time")
col1, col2 = st.columns([2, 0.8])
with col1:
    if os.path.exists(mpg_growth_rate_path):
        st.image(mpg_growth_rate_path, width=1200)
    else:
        st.error(f"Plot not found: {mpg_growth_rate_path}")
with col2:
    explanation = get_explanation(selected_manufacturer, "MPG Growth")
    st.markdown(
        f"""
        <div>
            <p style="font-size: 15px; line-height: 2.0;">
                {explanation}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Display powertrain distribution pie chart with description box
st.subheader("Powertrain Distribution")
col1, col2 = st.columns([2, 0.8])
with col1:
    if os.path.exists(powertrain_pie_chart_path):
        st.image(powertrain_pie_chart_path, width=1200)
    else:
        st.error(f"Plot not found: {powertrain_pie_chart_path}")
with col2:
    explanation = get_explanation(selected_manufacturer, "Powertrain")
    st.markdown(
        f"""
        <div>
            <p style="font-size: 15px; line-height: 2.0;">
                {explanation}
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

st.subheader("🤖 AI Sentiment Analysis")
if st.button("⚡ Run Sentiment Analysis"):
    pdf_path = f"sustainability_reports/{selected_manufacturer} Sustainability Report.pdf"

    # Invalidate and update cache
    update_cache_metadata()

    if os.path.exists(pdf_path):
        with st.spinner("Running sentiment analysis. Please be patient, this may take a few moments..."):
            from ai_sentiment_analysis import main as sentiment_analysis
            final_score, explanation = sentiment_analysis(selected_manufacturer, sustainability_score, pdf_path=pdf_path)

            st.success(f"✅ Adjusted Sustainability Score: **{final_score:.2f}**")
            st.markdown(
                f"""
                <div style="padding: 15px; border-radius: 10px; border: 1px solid #ffffff;">
                    <h4 style="color:#ffffff;">Explanation:</h4>
                    <p style="font-size: 16px; color:#ffffff;">{explanation}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.error(f"❌ PDF not found for {selected_manufacturer}.")