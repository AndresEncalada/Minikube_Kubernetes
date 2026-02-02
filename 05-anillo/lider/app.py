from flask import Flask, request, jsonify
import requests
import os
import threading

app = Flask(__name__)
my_name = "Servicio-A"

# Configuración: A quién le paso la bola (Servicio B)
NEXT_SERVICE = os.getenv("NEXT_SERVICE", "http://servicio-b:5000")

@app.route('/')
def index():
    return "<h1>Soy el Servicio A. Usa /start para iniciar el anillo.</h1>"

# 1. INICIO: Tú (usuario) llamas aquí para empezar el juego
@app.route('/start')
def start_ring():
    payload = {"mensaje": "Hola", "camino": [my_name]}
    
    print(f"--> {my_name} iniciando anillo hacia {NEXT_SERVICE}")
    
    # Lanzamos la petición en un hilo aparte para no bloquear al navegador
    def enviar():
        try:
            requests.post(f"{NEXT_SERVICE}/relay", json=payload)
        except Exception as e:
            print(f"Error contactando al siguiente: {e}")
            
    threading.Thread(target=enviar).start()
    
    return jsonify({"status": "Anillo iniciado. Mira los logs del pod!"})

# 4. FIN: El último servicio (C) llama aquí para terminar
@app.route('/finish', methods=['POST'])
def finish_ring():
    data = request.json
    camino_final = data.get('camino', [])
    print(f"✅ ANILLO COMPLETADO. La bola pasó por: {camino_final}")
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)