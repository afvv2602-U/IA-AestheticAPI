from flask import Flask, request, jsonify
import torch
import torchvision.transforms as transforms
from PIL import Image
import io

app = Flask(__name__)

# Cargar el modelo
model_path = 'Model/complete_model.pth'
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

# Función para predecir la clase de la imagen
class_names = ['Barroco', 'Cubismo', 'Expresionismo', 'Impresionismo', 'Realismo', 'Renacimiento', 'Rococo', 'Romanticismo']

@app.route('/predict', methods=['POST'])
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
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
