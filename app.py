from flask import Flask, request, jsonify, render_template_string
from werkzeug.exceptions import HTTPException
import ssl

app = Flask(__name__)

# Define una clave API segura
API_KEY = "IRfzQeWjngxQWyfVP0xa-Ee4f5WPtJtZ_XeBLuu8-PE"

# Página de inicio
@app.route('/')
def home():
    return render_template_string("<h1>Esta es la API de Aesthetica</h1>")

# Autenticación con API Key
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
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No file provided"}), 400

    # Aquí iría tu lógica de predicción con el modelo

    return jsonify({"result": "prediction result"})

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