# Carbon Lens Dashboard

## Overview

The **Carbon Lens Dashboard** is an AI-powered application designed to assess and analyze the sustainability of automotive manufacturers and individual car models. This tool integrates advanced AI models, machine learning, and sentiment analysis to provide insightful sustainability scores and trends, helping users understand environmental impacts across the automotive industry.

---

## Features

1. **AI-Powered Car Sustainability Analysis**:
   - Upload car images or input car model names to evaluate their sustainability.
   - Scores and explanations are generated based on factors such as emissions, energy efficiency, and manufacturing practices.

2. **Manufacturer Analysis**:
   - Detailed visualizations for individual manufacturers, highlighting:
     - CO2 emissions over time.
     - Fuel efficiency (MPG) growth.
     - Sustainability trends and forecasts using **Prophet**.
     - Powertrain distribution for advanced insights.

3. **Sentiment-Enhanced Adjustments**:
   - Combines **Reddit discussions** and **manufacturer sustainability reports** to enhance score accuracy using **sentiment analysis**.
   - Sentiment scores influence final evaluations for a holistic perspective.

4. **Machine Learning-Based Predictions**:
   - Uses a **Random Forest model** to predict sustainability scores based on real-world emissions, MPG, and powertrain contributions.

---

## Data Sources

- **United States Environmental Protection Agency (EPA)**: Primary source for emissions and MPG data.
- **Reddit API**: Provides public sentiment analysis regarding manufacturers’ sustainability initiatives.
- **Manufacturer Sustainability Reports**: Extracted for internal insights on initiatives and commitments.

---

## Why Sustainability Scores Matter

Sustainability metrics help combat climate change and foster eco-friendly innovations in the automotive industry. Manufacturers can leverage insights to:
- Comply with global regulations.
- Build consumer trust.
- Contribute to reducing the industry's environmental footprint.

---

## Key Components

### **1. Home Page (🗂️ Home Page)**
- Introduces the project and provides an overview of automotive sustainability trends.
- Includes comparative visualizations, such as boxplots for manufacturer scores and trends over time.

### **2. Manufacturer Analysis (📈 Manufacturer Analysis)**
- Detailed insights for individual manufacturers:
  - Sustainability score forecasts.
  - Real-world CO2 emissions and MPG trends.
  - Powertrain distribution analysis.
- AI sentiment analysis integration.

### **3. AI Car Sustainability Analyzer (🚗 AI Car Sustainability Analyzer)**
- Analyze the sustainability of car models using:
  - **CLIP Model** for car image recognition.
  - **Cohere API** to generate sustainability scores and explanations.

### **4. Advanced Visualizations (manufacturer_advanced_visuals.py, visualizations.py)**
- Generates advanced insights:
  - CO2 reduction rates.
  - MPG efficiency growth.
  - Powertrain composition.

### **5. Future Predictions (future_predictions.py)**
- Uses **Prophet** to forecast sustainability scores for manufacturers based on historical trends.

### **6. Machine Learning (random_forest_model.py)**
- A Random Forest model predicts yearly sustainability scores using weighted features:
  - CO2 emissions, MPG, and powertrain contributions.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/carbon-lens-dashboard.git
   cd carbon-lens-dashboard
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit app:
   ```bash
   streamlit run 🗂️_Home_Page.py
   ```

---

## How It Works

1. **Data Processing**:
   - Filters emissions data from 2008 onward for consistent analysis.
   - Normalizes metrics like CO2 emissions and MPG for comparability.

2. **AI Models**:
   - **CLIP**: Identifies car models from uploaded images.
   - **Cohere API**: Generates sustainability scores with detailed explanations.
   - **DistilBERT**: Performs sentiment analysis on Reddit posts and reports.

3. **Machine Learning**:
   - Random Forest predicts sustainability scores with cross-validation for reliability.

4. **Prophet Forecasting**:
   - Predicts sustainability trends for manufacturers over the next decade.

---

## Example Insights

- **CO2 Emissions**:
  - Graphs highlight the reduction in emissions over time for major manufacturers.
- **Sustainability Scores**:
  - Provides a clear comparison of efforts between brands like Toyota, Hyundai, and Volkswagen.
- **Future Predictions**:
  - Highlights expected sustainability improvements based on past performance.

---

## Dependencies
This project requires the following:

- **Python 3.7+**
- **Streamlit**: Interactive user interface.
- **Matplotlib**: Data visualizations.
- **NumPy**: Numerical processing.
- **Pandas**: Data handling and analysis.
- **Cohere API**: NLP-powered sustainability explanations.
- **CLIP (OpenAI)**: Car image recognition.
- **Prophet**: Time series forecasting.
- **Scikit-learn**: Machine learning predictions.
- **Pillow**: Image processing for CLIP.
- **Pdfplumber**: Extracting text from PDFs (e.g., sustainability reports).
- **PRAW**: Sentiment analysis using Reddit data.

To install all dependencies, run:
```bash
pip install -r requirements.txt
```

---

## Disclaimer

This tool is for educational purposes and does not aim to critique or promote any specific manufacturer. All data is sourced from public records, including the **EPA** and Reddit. Tesla was excluded due to insufficient comparable data, ensuring consistent analysis.

---

## License

This project is open-source and available under the [MIT License](LICENSE).

---
