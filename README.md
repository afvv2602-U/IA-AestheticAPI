# IA Art Classification API

Este repositorio contiene una API desarrollada con Flask que utiliza un modelo de Deep Learning 
entrenado para clasificar imágenes de arte en diferentes movimientos artísticos. 
La API está diseñada para ejecutarse en una Raspberry Pi con Debian.


## Requisitos

- Raspberry Pi con Debian instalado
- Python 3.7 o superior
- pip y virtualenv

## Generar API 

- En el archivo de Utils generate_api_key generamos una clave para poner en el archivo de config.py

## Exportar la clave API

export API_KEY=your_generated_api_key_here

## General certificados

- Linux
* openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365

- Windows
* Instala OpenSSL y ejecuta el mismo comando en la línea de comandos de Windows.

Este comando generará dos archivos: key.pem (clave privada) y cert.pem (certificado).

## Uso raspberry 

- source myenv/bin/activate
- pip install -r requirements.txt
- python app.py


## Uso version de la API sin securizar

- curl -X POST -F "file=@/path/to/your/image.jpg" http://0.0.0.0:5000/predict


## Uso version de la API Securizada

- curl -X POST https://aesthetica.myvnc.com:10900/predict \
  -H "x-api-key: IRfzQeWjngxQWyfVP0xa-Ee4f5WPtJtZ_XeBLuu8-PE" \
  -F "file=@/path/to/your/image.jpg" -k


## Activar servidor WSGI

- gunicorn --bind 0.0.0.0:10900 \
  --certfile=/etc/letsencrypt/live/aesthetica.myvnc.com/fullchain.pem \
  --keyfile=/etc/letsencrypt/live/aesthetica.myvnc.com/privkey.pem \
  --timeout 120 \
  --workers 4 \
  --log-level debug \
  --log-file /home/randy/Documents/API/gunicorn.log \
  wsgi:app
