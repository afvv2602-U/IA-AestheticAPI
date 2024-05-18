# IA Art Classification API

Este repositorio contiene una API desarrollada con Flask que utiliza un modelo de Deep Learning 
entrenado para clasificar imágenes de arte en diferentes movimientos artísticos. 
La API está diseñada para ejecutarse en una Raspberry Pi con Debian.

## Requisitos

- Raspberry Pi con Debian instalado
- Python 3.7 o superior
- pip y virtualenv

## Uso

curl -X POST -F "file=@/path/to/your/image.jpg" http://0.0.0.0:5000/predict


