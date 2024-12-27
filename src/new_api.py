import tensorflow as tf
from flask import Flask, request, jsonify
import openai
import numpy as np
from PIL import Image

app = Flask(__name__)

# Load car recognition model
model = tf.keras.models.load_model("car_recognition_model.h5")

# AI scoring function
def get_sustainability_score_from_ai(car_model):
    openai.api_key = "your_openai_api_key"
    prompt = f"Analyze the sustainability of the car model: {car_model}. Provide a score between 0-100 and an explanation."
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    message = response.choices[0].text.strip()
    score = int([int(s) for s in message.split() if s.isdigit()][0])
    explanation = message.split(". ", 1)[-1]
    return score, explanation

# Image preprocessing function
def preprocess_image(image):
    img = Image.open(image).convert('RGB').resize((224, 224))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

# API endpoint for car analysis
@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        car_model = data.get("car_model")
        if not car_model and 'file' not in request.files:
            return jsonify({"error": "Car model or image file is required."}), 400

        if car_model:
            # Use AI scoring for car model name
            score, explanation = get_sustainability_score_from_ai(car_model)
        else:
            # Use car recognition model for image input
            file = request.files['file']
            img_array = preprocess_image(file)
            predictions = model.predict(img_array)
            predicted_class = np.argmax(predictions, axis=1)[0]
            car_model = "Car Model Placeholder"  # Map predicted_class to car model
            score, explanation = get_sustainability_score_from_ai(car_model)

        return jsonify({"car_model": car_model, "sustainability_score": score, "details": explanation})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)