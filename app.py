from flask import Flask, request, jsonify
import joblib

# Load the model
model = None
try:
    model = joblib.load('./SavedModels/crop.joblib')
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading the model: {e}")

# Region
Regions = {
    'Barley': 'Barley is suitable to grow in Taran Taran near Sutlej River or in the Roop Nagar near Ghaggar-Hakra River or in the Pathankot near Ravi River.',
    'Beans': 'Beans is suitable to grow in Taran Taran near Sutlej River.',
    'Corn': 'Corn is suitable to grow in Taran Taran near Sutlej River or in the Kapurthala near Beas River or in the Roop Nagar near Ghaggar-Hakra River or in the Pathankot near Ravi River.',
    'Cauliflower': 'Cauliflower is suitable to grow in Taran Taran near Sutlej River or in the Kapurthala near Beas River.',
    'Lentils': 'Lentils is suitable to grow in Taran Taran near Sutlej River.',
    'Lettuce': 'Lettuce is suitable to grow in Taran Taran near Sutlej River.',
    'Mustard': 'Mustard is suitable to grow in the Kapurthala near Beas River.',
    'Oranges': 'Oranges is suitable to grow in the Kapurthala near Beas River.',
    'Peas': 'Peas is suitable to grow in Taran Taran near Sutlej River.',
    'Peppers': 'Peppers is suitable to grow in Taran Taran near Sutlej River.',
    'Potatoes': 'Potato is suitable to grow in Taran Taran near Sutlej River or in the Kapurthala near Beas River.',
    'Pulses': 'Pulses is suitable to grow in Taran Taran near Sutlej River or in the Kapurthala near Beas River or in the Roop Nagar near Ghaggar-Hakra River or in the Pathankot near Ravi River.',
    'Rice': 'Rice is suitable to grow in Taran Taran near Sutlej River or in the Roop Nagar near Ghaggar-Hakra River or in the Pathankot near Ravi River.',
    'Sorghum': 'Sorghum is suitable to grow in Taran Taran region near Sutlej River or in the Roop Nagar near Ghaggar-Hakra River.',
    'Spinach': 'Spinach is suitable to grow in Taran Taran near Sutlej River.',
    'Sugarcane': 'Sugarcane is suitable to grow in Taran Taran region near Sutlej River or in the Kapurthala near Beas River or in the Roop Nagar near Ghaggar-Hakra River or in the Pathankot near Ravi River.',
    'Sunflower': 'Sunflower is suitable to grow in Taran Taran near Sutlej River or in the Kapurthala near Beas River.',
    'Tomatoes': 'Tomatoes is suitable to grow in Taran Taran region near Sutlej River or in the Kapurthala near Beas River or in the Roop Nagar near Ghaggar-Hakra River or in the Pathankot near Ravi River.',
    'Wheat': 'Wheat is suitable to grow in Taran Taran region near Sutlej River or in the Kapurthala near Beas River or in the Roop Nagar near Ghaggar-Hakra River or in the Pathankot near Ravi River.',
}

# Create the Flask app
app = Flask(__name__)

@app.route("/")
def home():
    return "Server is running."

@app.route("/", methods=["POST"])
def predict():
    try:
        # Get input data from request
        data = request.json
        
        # Perform prediction using the loaded model
        input_features = [
            float(data.get("N", 0)), 
            float(data.get("P", 0)), 
            float(data.get("K", 0)), 
            float(data.get("ph", 0)), 
            float(data.get("temperature", 0)), 
            float(data.get("moisture", 0))
        ]
        prediction = model.predict([input_features])
        
        # Map prediction to crop name
        crop_names = [
            'Barley', 'Beans', 'Corn', 'Cauliflower', 'Lentils', 'Lettuce', 
            'Mustard', 'Oranges', 'Peas', 'Peppers', 'Potatoes', 'Pulses', 
            'Rice', 'Sorghum', 'Spinach', 'Sugarcane', 'Sunflower', 'Tomatoes', 'Wheat'
        ]
        if 0 <= prediction[0] < len(crop_names):
            crop = crop_names[prediction[0]]
            Region = Regions.get(crop, 'No specific regions available.')
        else:
            crop = 'Soil is not fit for growing crops',
            Region = 'none'
        
        response = {
            "prediction": crop,
            "Region":Region
        }
        
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
