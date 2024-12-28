from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import streamlit as st
import cohere
import io

# Load pretrained CLIP model and processor
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# Expanded car_labels with 500 popular car models
car_labels = [
    "Hyundai Tucson", "Toyota Camry", "Honda Civic", "Mercedes-Benz E-Class", "BMW 5 Series", "Ford Mustang", 
    "BMW 3 Series", "Audi A4", "Tesla Model 3", "Chevrolet Malibu", "Nissan Altima", "Volkswagen Passat",
    "Jeep Grand Cherokee", "Subaru Outback", "Mazda CX-5", "Porsche Cayenne", "Kia Sportage", "Jaguar XF",
    "Honda Accord", "Toyota Corolla", "Chevrolet Equinox", "Ford Explorer", "Toyota RAV4", "Hyundai Elantra",
    "Mazda 3", "Kia Soul", "Subaru Impreza", "Volkswagen Jetta", "Chevrolet Traverse", "GMC Acadia",
    "Jeep Wrangler", "Toyota Highlander", "Ford Escape", "Nissan Rogue", "Chevrolet Tahoe", "Lexus RX",
    "BMW X5", "Audi Q5", "Mercedes-Benz GLC", "Honda CR-V", "Hyundai Santa Fe", "Volvo XC60", "Range Rover Evoque",
    "Toyota Tacoma", "Ford F-150", "Chevrolet Silverado", "Ram 1500", "GMC Sierra", "Nissan Titan",
    "Dodge Charger", "Chrysler 300", "Cadillac CT5", "Porsche 911", "Tesla Model S", "Tesla Model Y",
    "Lexus ES", "Acura TLX", "Infiniti Q50", "Genesis G70", "Genesis G80", "Alfa Romeo Giulia",
    "Mini Cooper", "Fiat 500", "Mazda MX-5 Miata", "Chevrolet Corvette", "Ford Bronco", "Kia Telluride",
    "Hyundai Palisade", "Toyota Land Cruiser", "Land Rover Defender", "Audi A6", "BMW 7 Series", "Mercedes-Benz S-Class",
    "Bentley Continental", "Rolls-Royce Ghost", "Aston Martin DB11", "Ferrari 488", "Lamborghini Huracan",
    "McLaren 720S", "Porsche Panamera", "Jaguar F-Type", "Maserati Ghibli", "Bugatti Chiron",
    "Nissan Leaf", "Chevrolet Bolt", "Hyundai Kona Electric", "Kia Niro EV", "BMW i3", "Audi e-tron",
    "Jaguar I-Pace", "Ford Mach-E", "Rivian R1T", "Lucid Air", "Polestar 2", "Volkswagen ID.4",
    "Subaru Crosstrek", "Mazda CX-30", "Kia Seltos", "Hyundai Venue", "Toyota C-HR", "Honda HR-V",
    "Jeep Renegade", "Chevrolet Trax", "Ford EcoSport", "Nissan Kicks", "Mitsubishi Outlander",
    "Hyundai Ioniq", "Honda Insight", "Toyota Prius", "Kia Optima", "Mazda 6", "Ford Fusion",
    "Chrysler Pacifica", "Honda Odyssey", "Toyota Sienna", "Kia Carnival", "Dodge Grand Caravan",
    "Nissan Murano", "Chevrolet Blazer", "Ford Edge", "Volkswagen Atlas", "BMW X3", "Audi Q7",
    "Mercedes-Benz GLE", "Volvo XC90", "Lexus NX", "Tesla Cybertruck", "Ford Maverick", "Hyundai Santa Cruz",
    "Toyota Supra", "Ford GT", "Chevrolet Camaro", "Dodge Challenger", "Nissan 370Z",
    "Mitsubishi Eclipse Cross", "Suzuki Swift", "Peugeot 208", "Renault Clio", "Fiat Panda",
    "Citroën C3", "Skoda Octavia", "Seat Leon", "Volkswagen Golf", "Opel Corsa",
    "Honda Jazz", "Toyota Yaris", "Hyundai i20", "Kia Rio", "Ford Fiesta",
    "Mazda CX-9", "Toyota Venza", "Subaru Ascent", "Volkswagen Tiguan", "GMC Terrain",
    "Lexus GX", "Land Rover Discovery", "Audi Q8", "BMW X7", "Mercedes-Benz GLS",
    "Rolls-Royce Cullinan", "Bentley Bentayga", "Lamborghini Urus", "Ferrari Purosangue",
    "Chevrolet Suburban", "Ford Expedition", "Nissan Armada", "Toyota Sequoia", "Hyundai Ioniq 5",
    "Kia EV6", "Tesla Model X", "Rivian R1S", "Lucid Gravity", "Volkswagen ID. Buzz"
]

# Initialize Cohere API
co = cohere.Client('jgqeITEBHzYLimbQnsay4dH7uIJIDaSA6QYUUZIz')

# Cohere Sustainability Scoring
def get_sustainability_score(car_model):
    prompt = f"Analyze the sustainability of '{car_model}' and give a score (0-100) with a short explanation."
    response = co.generate(
        model='command-xlarge-nightly',
        prompt=prompt,
        max_tokens=200,
        temperature=0.7
    )
    result = response.generations[0].text.strip()
    return result

# Preprocess Image
def preprocess_image(image):
    img = Image.open(image).convert("RGB").resize((224, 224))
    inputs = processor(images=img, text=car_labels, return_tensors="pt", padding=True)
    outputs = model(**inputs)
    logits_per_image = outputs.logits_per_image
    probs = logits_per_image.softmax(dim=1)
    predicted_idx = probs.argmax().item()
    return car_labels[predicted_idx]

# Streamlit App
st.set_page_config(page_title="AI Car Sustainability Analysis", page_icon="🚗", layout="wide")
st.title("🚗 Car Sustainability Analyzer")

# Input Options
input_method = st.radio("Choose an input method:", ("Upload Car Image", "Enter Car Model"))

if input_method == "Upload Car Image":
    uploaded_file = st.file_uploader("Upload an image of the car:", type=["jpg", "jpeg", "png"])
    if uploaded_file and st.button("Analyze Image"):
        car_model = preprocess_image(uploaded_file)
        st.success(f"Predicted Car Model: {car_model}")
        result = get_sustainability_score(car_model)
        st.info("Sustainability Analysis:")
        st.write(result)

elif input_method == "Enter Car Model":
    car_model = st.text_input("Enter the car model (e.g., Toyota RAV4, Tesla Model 3):")
    if car_model and st.button("Analyze Model"):
        if car_model in car_labels:
            result = get_sustainability_score(car_model)
            st.info("Sustainability Analysis:")
            st.write(result)
        else:
            st.error("Car model not recognized. Please check your input.")