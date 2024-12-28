# 🚗 Car Sustainability Analyzer

## 📖 Overview

The **Car Sustainability Analyzer** is an AI-powered tool that evaluates the sustainability of car models based on factors such as emissions, materials, energy efficiency, and manufacturing practices. Users can upload a car image or input a car model to receive a **Sustainability Score** and a detailed explanation.

This project combines **AI image recognition** for car model identification with **Cohere's NLP API** to generate sustainability scores and explanations. It aims to promote awareness about vehicle sustainability without targeting any specific manufacturer.

---

## 🛠️ Features

- **Car Model Identification:** Upload a car image, and the tool predicts the car model using a trained **CLIP model**.
- **Sustainability Score:** Analyzes key environmental factors to generate a sustainability score and detailed explanation using the **Cohere API**.
- **Manual Input Option:** Users can manually correct the car model if the prediction is inaccurate.
- **Visual Insights:** Interactive graphs display sustainability trends across manufacturers and years.

---

## 🚀 How to Use

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/car-sustainability-analyzer.git
   cd car-sustainability-analyzer
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```
4. Upload a car image or input a car model to analyze its sustainability.

---

## 📊 Data Sources

This project strictly uses publicly available data, including data from the **United States Environmental Protection Agency (EPA)**. 

---

## ⚠️ Disclaimer

This project is intended for educational purposes only. The sustainability scores are based on publicly available data and are not meant to critique or promote specific manufacturers. **Tesla** was excluded from the analysis due to a lack of comparable data, ensuring a fair and standardized evaluation across all manufacturers.

---

## 🖼️ Example Output

1. **Sustainability Analysis for BMW X7:**
   - Sustainability Score: 65/100
   - Explanation: Includes analysis of emissions, materials, and manufacturing efficiency.

2. **Graphs:**
   - **Sustainability Growth Over Time** for all manufacturers.
   - Boxplots showing **yearly sustainability scores** across brands.

---

## 📦 Dependencies

- Python 3.7+
- `streamlit`
- `matplotlib`
- `numpy`
- `pandas`
- `cohere`
- `clip` (from OpenAI)

---

## 🤝 Acknowledgments

Special thanks to:
- **United States Environmental Protection Agency** for providing public data.
- **Cohere** for the NLP API to generate sustainability explanations.
- **OpenAI** for the CLIP model used in car recognition.

---

## 📝 License

This project is open-source and available under the [MIT License](LICENSE).

---

Feel free to adjust this based on your project specifics!