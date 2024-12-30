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
                This boxplot illustrates the yearly sustainability score distributions for various car manufacturers, highlighting their 
                efforts in emissions reduction, energy efficiency, and eco-friendly practices. The boxes represent the interquartile range (IQR), 
                with outliers indicating exceptional performance or setbacks. Toyota and Hyundai display consistent sustainability improvements, 
                while outliers suggest innovation. The variation in scores reflects diverse strategies and challenges faced by manufacturers in 
                transitioning toward sustainable practices.
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
                This graph depicts the sustainability scores of major car manufacturers from 2008 to 2024, reflecting their progress 
                in emissions reduction, energy efficiency, and eco-friendly initiatives. A steady rise across most manufacturers 
                indicates growing efforts toward sustainability, with a significant post-2020 surge due to increased EV adoption and 
                stricter regulations. Leaders like BMW and Mercedes show rapid advancements, setting benchmarks for the industry. The upward 
                trends highlight the global automotive sector's commitment to addressing environmental concerns, showcasing its 
                transition toward greener practices and technologies.
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
                This tool analyzes car manufacturers' sustainability using publicly available data, including information from the United States Environmental Protection Agency (EPA). 
                Scores reflect rigorous metrics, focusing on emissions, energy efficiency, and sustainability efforts. Tesla was excluded due to a lack of comparable 
                data, ensuring fairness and consistency in the analysis. This project aims to promote transparency and awareness, not to critique or target any 
                specific company.
            </p>
        </div>
        """,
        unsafe_allow_html=True
)
