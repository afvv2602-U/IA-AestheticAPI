from flask import Flask, request, jsonify, abort, render_template
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from PIL import Image
import io
import ssl
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Decorador para requerir API Key
def require_api_key(f):
    def decorated_function(*args, **kwargs):
        if request.headers.get('x-api-key') != app.config['API_KEY']:
            abort(401)
        return f(*args, **kwargs)
    return decorated_function

# Ruta al modelo
model_path = 'path/to/your/model/complete_model.pth'

# Cargar el modelo
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = torch.load(model_path)
model.to(device)
model.eval()

# Transformaciones para la imagen
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

class_names = ['Barroco', 'Cubismo', 'Expresionismo', 'Impresionismo', 'Realismo', 'Renacimiento', 'Rococo', 'Romanticismo']

@app.route('/')
def home():
    return render_template('index.html')

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
        return jsonify({'error': 'An error occurred'}), 500

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({'error': 'Unauthorized access'}), 401

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({'error': 'An internal error occurred'}), 500

if __name__ == '__main__':
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile='cert.pem', keyfile='key.pem')
    app.run(host='0.0.0.0', port=10900, ssl_context=context)
