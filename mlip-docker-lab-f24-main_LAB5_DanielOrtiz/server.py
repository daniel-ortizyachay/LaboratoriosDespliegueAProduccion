from flask import Flask, request, jsonify
import numpy as np
import joblib

app = Flask(__name__)

# Load the trained model from the shared volume (use the correct path)
model = joblib.load('./models/iris_model.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    # Get the input array from the request body
    data = request.get_json()
    iris_input = data['input']

    # Make prediction using the model
    # Convert input to 2D array
    prediction = model.predict(np.array(iris_input).reshape(1, -1))

    # Return the prediction as a response
    return jsonify({'prediction': prediction.tolist()})

@app.route('/')
def hello():
    return 'Welcome to Docker Lab'

if __name__ == '__main__':
    # Run the Flask app (bind it to port 8080)
    app.run(debug=True, port=8080, host='0.0.0.0')
