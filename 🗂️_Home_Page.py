import streamlit as st
from PIL import Image
import os

# Set the page configuration
st.set_page_config(page_title="Home - Carbon Lens", page_icon="♻️", layout="wide")

# Page Title
st.title("🌟 Welcome to the Carbon Lens Dashboard")
st.markdown("""
This dashboard provides insights into automotive manufacturers' sustainability efforts and individual car models' environmental impacts. 
Through advanced AI and data analysis, we evaluate key metrics to generate sustainability scores and trends.
""")

# About the Project
st.header("🚀 About the Project")
st.markdown("""
Sustainability is a key factor in the automotive industry as manufacturers transition to environmentally friendly technologies.
This dashboard helps track and analyze sustainability scores based on key metrics such as:
- **CO2 Emissions**: Real-world carbon emissions in grams per mile.
- **Fuel Economy (MPG)**: Efficiency in miles per gallon, including real-world Ton-MPG metrics.
- **Powertrain Type**: Gasoline, hybrid, and electric powertrains are considered.
- **Yearly Sustainability Trends**: Tracks the improvement or decline in sustainability over the years.
""")

# Why Sustainability Scores Matter
st.header("🌍 Why Are Sustainability Scores Important?")
st.markdown("""
Understanding and improving sustainability metrics in the automotive industry is vital for combating climate change. 
By focusing on reducing emissions and improving efficiency, manufacturers can:
- Comply with global environmental regulations.
- Enhance consumer trust and brand image.
- Contribute to a healthier planet for future generations.
""")

# Display Key Overall Visuals
st.header("📊 Key Visual Insights")
st.markdown("Below are some overall insights into manufacturers' sustainability efforts.")

# Display Comparative Boxplot
st.subheader("Comparative Sustainability Score Boxplot")
boxplot_path = "manufacturer_advanced_visuals/comparative_sustainability_boxplot.png"
col1, col2 = st.columns([2, 0.5])
with col1:
    if os.path.exists(boxplot_path):
        st.image(boxplot_path, width=1500)
    else:
        st.error(f"Plot not found: {boxplot_path}")
with col2:
    st.markdown(
        f"""
        <div>
            <p style="font-size: 12px; line-height: 2.0;">
                This boxplot shows yearly sustainability score distributions for car manufacturers, reflecting emissions reduction, energy efficiency, and eco-friendly practices. 
                Toyota and Hyundai show consistent improvements, with outliers highlighting innovation. Variations indicate the diverse strategies and challenges of achieving sustainability goals.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Display Top Sustainability Efforts
st.subheader("Manufacturers' Sustainability Growth Over Time")
top_efforts_path = "manufacturer_advanced_visuals/all_manufacturers_sustainability_growth_updated.png"

col1, col2 = st.columns([2, 0.5])
with col1:
    if os.path.exists(top_efforts_path):
        st.image(top_efforts_path, width=1500)
    else:
        st.error(f"Plot not found: {top_efforts_path}")
with col2:
    st.markdown(
        f"""
        <div>
            <p style="font-size: 12px; line-height: 2.0;">
                This graph illustrates the sustainability scores of major car manufacturers (2008-2024), highlighting progress in emissions reduction, energy efficiency, and eco-friendly initiatives. 
                Post-2020, scores surged due to EV adoption and stricter regulations, with leaders like BMW and Mercedes setting benchmarks in green practices.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

st.subheader("⚠️ Disclaimer")
st.markdown(
    f"""
        <div>
            <p style="font-size: 12px; line-height: 2.0;">
                This tool uses publicly available data from the United States Environmental Protection Agency (EPA). Scores are unbiased, reflecting manufacturers' true environmental impact based on rigorous metrics. 
                Tesla was excluded due to a lack of comparable data. The project promotes transparency and awareness, not criticism or targeting of specific companies.
            </p>
        </div>
        """,
        unsafe_allow_html=True
)
