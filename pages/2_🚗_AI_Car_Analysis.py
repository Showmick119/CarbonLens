import streamlit as st
from PIL import Image
import random

# Set the page configuration
st.set_page_config(page_title="AI Product Analysis", page_icon="🚗", layout="wide")

# Page Title
st.title("AI Product Analysis")
st.write("This tool allows you to generate a sustainability score for a car. Enter the car model name or upload an image, and the AI will predict its sustainability score and visualize it as a star rating.")

# User input for car model or image upload
st.subheader("Choose an Input Method")
input_method = st.radio("Select how you'd like to input your car details:", ("Enter Car Model Name", "Upload Car Image"))

# Generate a sustainability score (mockup logic)
def generate_sustainability_score(input_data):
    # Simulate sustainability score generation
    score = random.randint(20, 50)  # Mock score between 20 and 50
    return score

# Visualize sustainability score as stars
def visualize_score_as_stars(score):
    stars = "★" * (score // 10) + "☆" * (5 - score // 10)
    return stars

# Logic for car model name input
if input_method == "Enter Car Model Name":
    car_model = st.text_input("Enter the Car Model Name (e.g., Tesla Model 3, Ford F-150):")
    if st.button("Generate Sustainability Score"):
        if car_model:
            score = generate_sustainability_score(car_model)
            st.success(f"The sustainability score for {car_model} is: {score}/50")
            st.markdown(f"### {visualize_score_as_stars(score)} ({score / 10:.1f} stars)")
        else:
            st.error("Please enter a car model name.")

# Logic for image upload
elif input_method == "Upload Car Image":
    uploaded_image = st.file_uploader("Upload an image of the car:", type=["jpg", "jpeg", "png"])
    if st.button("Generate Sustainability Score"):
        if uploaded_image:
            image = Image.open(uploaded_image)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            score = generate_sustainability_score(uploaded_image)
            st.success(f"The sustainability score for the uploaded car is: {score}/50")
            st.markdown(f"### {visualize_score_as_stars(score)} ({score / 10:.1f} stars)")
        else:
            st.error("Please upload an image.")

# Footer
st.write("Note: This is a mock implementation for demonstration purposes. AI model integration can be added for real predictions.")