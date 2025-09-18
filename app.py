from flask import Flask, render_template, request, jsonify
import numpy as np
import joblib
import os

app = Flask(__name__)

# Load models (ensure these are in the working directory)
MODEL_FILE = "models\\svr_model.pkl"
SCALER_FILE = "models\\scaler_model.pkl"
PCA_FILE = "models\\pca_model.pkl"

model = joblib.load(MODEL_FILE)
scaler = joblib.load(SCALER_FILE)
pca = joblib.load(PCA_FILE)

# Fields & default values
FIELDS = [
    'Bicarbonate', 'Calcium', 'Chloride', 'Electrical_Conductance',
    'Magnesium', 'pH', 'Potassium', 'Sodium', 'Sulfur', 'Temperature'
]

DEFAULTS = {
    'Bicarbonate': 100,
    'Calcium': 50,
    'Chloride': 20,
    'Electrical_Conductance': 500,
    'Magnesium': 30,
    'pH': 7.0,
    'Potassium': 5,
    'Sodium': 40,
    'Sulfur': 15,
    'Temperature': 25
}

@app.route('/')
def index():
    return render_template('index.html', fields=FIELDS, defaults=DEFAULTS)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json  # must be JSON
        values = [float(data[field]) for field in FIELDS]
        values = np.array(values).reshape(1, -1)
        scaled = scaler.transform(values)
        reduced = pca.transform(scaled)
        prediction = model.predict(reduced)[0]
        return jsonify({'tds': round(float(prediction), 2)})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)