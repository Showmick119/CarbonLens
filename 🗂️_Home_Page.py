import streamlit as st
from PIL import Image

# Set the page configuration
st.set_page_config(page_title="Home - Carbon Lens", page_icon="🗂️", layout="wide")

# Page Title
st.title("Welcome to the Sustainability Analysis Dashboard")
st.markdown("""
This dashboard provides insights into automotive manufacturers' sustainability efforts and individual car models' environmental impacts. 
Through advanced AI and data analysis, we evaluate key metrics to generate sustainability scores and trends.
""")

# About the Project
st.header("About the Project")
st.markdown("""
Sustainability is a key factor in the automotive industry as manufacturers transition to environmentally friendly technologies.
This dashboard helps track and analyze sustainability scores based on key metrics such as:
- **CO2 Emissions**: Real-world carbon emissions in grams per mile.
- **Fuel Economy (MPG)**: Efficiency in miles per gallon, including real-world Ton-MPG metrics.
- **Powertrain Type**: Gasoline, hybrid, and electric powertrains are considered.
- **CO2-to-MPG Ratio**: Highlights the efficiency of a car in relation to its emissions.
- **Yearly Sustainability Trends**: Tracks the improvement or decline in sustainability over the years.
""")

# Why Sustainability Scores Matter
st.header("Why Are Sustainability Scores Important?")
st.markdown("""
Understanding and improving sustainability metrics in the automotive industry is vital for combating climate change. 
By focusing on reducing emissions and improving efficiency, manufacturers can:
- Comply with global environmental regulations.
- Enhance consumer trust and brand image.
- Contribute to a healthier planet for future generations.
""")

# Display Key Overall Visuals
st.header("Key Visual Insights")
st.markdown("Below are some overall insights into manufacturers' sustainability efforts.")

# Display Comparative Boxplot
st.subheader("Comparative Sustainability Score Boxplot")
boxplot_path = "manufacturer_advanced_visuals/comparative_sustainability_boxplot.png"
try:
    boxplot_img = Image.open(boxplot_path)
    st.image(boxplot_img, caption="Comparative Boxplot of Sustainability Scores", use_container_width=True)
except FileNotFoundError:
    st.error(f"Unable to load image at {boxplot_path}")

# Display Top Sustainability Efforts
st.subheader("Top Sustainability Efforts by Manufacturers")
top_efforts_path = "manufacturer_advanced_visuals/top_sustainability_efforts.png"
try:
    top_efforts_img = Image.open(top_efforts_path)
    st.image(top_efforts_img, caption="Top Sustainability Efforts by Manufacturers", use_container_width=True)
except FileNotFoundError:
    st.error(f"Unable to load image at {top_efforts_path}")

# Footer
st.write("Explore the other pages for detailed manufacturer-wise and AI-driven car sustainability analysis.")