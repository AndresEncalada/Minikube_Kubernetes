from flask import Flask, jsonify
import os

app = Flask(__name__)

# Requisito: Leer variable de entorno
COLOR = os.getenv("APP_COLOR", "unknown")

@app.route('/api/info')
def info():
    return jsonify({
        "mensaje": "Hola desde el Backend",
        "color_secreto": COLOR,
        "status": "Conectado exitosamente"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)