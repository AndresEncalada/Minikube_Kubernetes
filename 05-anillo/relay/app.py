from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# ¿Quién soy yo? (Lo sacamos del nombre del pod o variable)
MY_NAME = os.getenv("MY_NAME", "Desconocido")
# ¿A quién se lo paso?
NEXT_SERVICE = os.getenv("NEXT_SERVICE", "http://localhost:5000")
# ¿Soy el último antes del líder? (Para saber a qué endpoint llamar)
IS_LAST = os.getenv("IS_LAST", "no")

@app.route('/relay', methods=['POST'])
def relay_message():
    data = request.json
    
    # 1. Firmamos "Yo estuve aquí"
    data['camino'].append(MY_NAME)
    print(f"--> {MY_NAME} recibió la bola. Pasando a {NEXT_SERVICE}...")

    # 2. Decidimos a dónde llamar
    endpoint = "/relay"
    if IS_LAST == "yes":
        endpoint = "/finish" # Si soy el último, llamo al endpoint de fin del líder

    # 3. Pasamos la bola al siguiente
    try:
        requests.post(f"{NEXT_SERVICE}{endpoint}", json=data)
        return jsonify({"status": "pasado"})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)