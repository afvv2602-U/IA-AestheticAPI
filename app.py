import io
from flask import Flask, request, jsonify, render_template_string
from werkzeug.exceptions import HTTPException
import ssl
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from PIL import Image

app = Flask(__name__)

# Define a secure API key
API_KEY = "IRfzQeWjngxQWyfVP0xa-Ee4f5WPtJtZ_XeBLuu8-PE"

# Path to the model
model_path = 'model/complete_model.pth'

# Load the model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = torch.load(model_path, map_location=device)
model.to(device)
model.eval()

# Transformations for the image
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

class_names = ['Barroco', 'Cubismo', 'Expresionismo', 'Impresionismo', 'Realismo', 'Renacimiento', 'Rococo', 'Romanticismo']

# Home page
@app.route('/')
def home():
    return render_template_string("<h1>This is the Aesthetica API</h1>")

# API key authentication
def require_api_key(func):
    def decorated_function(*args, **kwargs):
        if request.headers.get('x-api-key') and request.headers.get('x-api-key') == API_KEY:
            return func(*args, **kwargs)
        else:
            return jsonify({"error": "Unauthorized"}), 401
    return decorated_function

@app.route('/predict', methods=['POST'])
@require_api_key
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file provided'}), 400

    try:
        img = Image.open(io.BytesIO(file.read()))
        img = transform(img).unsqueeze(0).to(device)

        with torch.no_grad():
            outputs = model(img)
            _, predicted = torch.max(outputs, 1)
            class_name = class_names[predicted.item()]

        return jsonify({'class_name': class_name}), 200
    except Exception as e:
        print(f"Error during prediction: {e}")
        return jsonify({'error': 'An error occurred'}), 500

@app.errorhandler(Exception)
def handle_exception(e):
    response = {
        "error": "An internal error occurred",
        "message": str(e)
    }
    if isinstance(e, HTTPException):
        response["code"] = e.code
    return jsonify(response), 500

if __name__ == '__main__':
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile='/etc/letsencrypt/live/aesthetica.myvnc.com/cert.pem',
                            keyfile='/etc/letsencrypt/live/aesthetica.myvnc.com/privkey.pem')
    app.run(host='0.0.0.0', port=10900, ssl_context=context)
