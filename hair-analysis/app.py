from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import os

app = Flask(__name__)
CORS(app)

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image_file = request.files['image']
    image_np = np.frombuffer(image_file.read(), np.uint8)
    img = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)

    white_pixels = np.sum(edges == 255)
    total_pixels = edges.size
    density_score = round((white_pixels / total_pixels) * 100, 2)

    if density_score > 5:
        health_status = "Healthy"
    elif density_score > 2:
        health_status = "Moderate"
    else:
        health_status = "Poor"

    return jsonify({
        'density_score': density_score,
        'health_status': health_status
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
