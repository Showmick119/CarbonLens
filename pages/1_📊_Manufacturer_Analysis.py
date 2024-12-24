import streamlit as st
import os

# Set the page configuration
st.set_page_config(page_title="Manufacturer Analysis", layout="wide")

# Page Title
st.title("Manufacturer Analysis")
st.write("Welcome to the Manufacturer Analysis page. Here you can explore sustainability efforts and metrics for different car manufacturers. Use the dropdown menu to select a manufacturer and view their detailed analysis.")

# Dropdown menu for selecting manufacturers
manufacturers = ['BMW', 'Ford', 'General Motors', 'Honda', 'Hyundai', 'Kia', 'Mazda', 'Mercedes', 'Nissan', 'Stellantis', 'Subaru', 'Toyota', 'VW']
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
                This graph shows the real-world (not under testing conditions) MPG from the cars of these manufacturers. This gives insights into these cars efficiency, and how many miles they are going per gallon consumed.
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

# Display MPG growth rate plot with description
st.subheader("MPG Growth Rate Over Time")
col1, col2 = st.columns([2, 0.8])
with col1:
    if os.path.exists(mpg_growth_rate_path):
        st.image(mpg_growth_rate_path, width=1200)
    else:
        st.error(f"Plot not found: {mpg_growth_rate_path}")
with col2:
    st.markdown(
        """
        <div>
            <p style="font-size: 20px; line-height: 2.0;">
                This graph indicates how much CO2 the vehicle is emitting, per mile driven. With lower values indicating more efficiency.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Display CO2-to-MPG ratio plot with description box

'''Problem: The CO2 and MPG values are not standardized to just be divided like that. It doesn't produce the most accurate of results.'''
'''Ideally, lower CO2 and higher MPG values are preferred. '''

st.subheader("CO2-to-MPG Ratio Over Time (Efficiency)")
col1, col2 = st.columns([2, 0.8])
with col1:
    if os.path.exists(co2_to_mpg_ratio_path):
        st.image(co2_to_mpg_ratio_path, width=1200)
    else:
        st.error(f"Plot not found: {co2_to_mpg_ratio_path}")
with col2:
    st.markdown(
        """
        <div>
            <p style="font-size: 20px; line-height: 2.0;">
                This graph indicates how much CO2 the vehicle is emitting, per mile driven. With lower values indicating more efficiency. No real improvement, 
                as we see no downward trend, and hence this is a metric the company needs to focus on, as it is harming its sustainability score and increasing
                its environmental impact.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

# AI Tool for Online Sentiment Analysis which will modify the Current Sustainability Score for this Manufacturer and return the final score
st.subheader("AI Sentiment Analysis")
st.write("This company follows these specific metrics and processes for their manufacturing and hence they get the following score for their sustainability and environmental impact")
st.write("Final Sustainability Score: 89/100")