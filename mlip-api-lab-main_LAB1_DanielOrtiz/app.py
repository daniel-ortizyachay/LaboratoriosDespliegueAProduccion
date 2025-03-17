from flask import Flask, request, jsonify, render_template
from analyze import read_image
import requests
import json

app = Flask(__name__, template_folder='templates')

@app.route("/")
def home():
    return render_template('index.html')


# API at /api/v1/analysis/ 
@app.route("/api/v1/analysis/", methods=['POST'])
def analysis():
    # Try to get the image file from the request
    if 'image' not in request.files:
        return jsonify({'error': 'No image file in request'}), 400
    
    image_file = request.files['image']
    
    # Try to get the text from the image
    try:
        res = read_image(image_file)
        
        response_data = {
            "text": res
        }
    
        return jsonify(response_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)