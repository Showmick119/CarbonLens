from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import os
import io
from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

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

# GPT Sustainability Scoring
openai.api_key = "your_openai_api_key"
def get_sustainability_score(car_model):
    prompt = f"Analyze the sustainability of the car model: {car_model}. Provide a score between 0-100 and an explanation."
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    result = response.choices[0].text.strip()
    score = int([int(s) for s in result.split() if s.isdigit()][0])
    explanation = result.split(". ", 1)[-1]
    return score, explanation

# Preprocess Image
def preprocess_image(image):
    img = Image.open(image).convert("RGB").resize((224, 224))
    return processor(images=img, return_tensors="pt", padding=True)

# Flask API Endpoint
@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json
        car_model = data.get("car_model")

        if not car_model:
            return jsonify({"error": "Car model name is required."}), 400

        score, explanation = get_sustainability_score(car_model)
        return jsonify({"car_model": car_model, "sustainability_score": score, "details": explanation})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)