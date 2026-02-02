from flask import Flask, request, jsonify
import requests
import os
import threading

app = Flask(__name__)

# --- CONFIGURACIÓN ---
MY_NAME = os.getenv("MY_NAME", "Nodo-Desconocido")
NEXT_SERVICE = os.getenv("NEXT_SERVICE", None)
IS_LAST = os.getenv("IS_LAST", "no")

# TIPO DE LÓGICA: ¿Qué soy? (upper, reverse, counter, logger)
LOGIC_TYPE = os.getenv("LOGIC_TYPE", "pass") 

# --- FUNCIONES DE LÓGICA DIFERENTE ---
def procesar_datos(data):
    mensaje = data.get("mensaje", "")
    contador = data.get("contador", 0)

    print(f"[{MY_NAME}] Procesando lógica: {LOGIC_TYPE}")

    if LOGIC_TYPE == "UPPER":
        # Lógica A: Convertir a Mayúsculas
        data["mensaje"] = mensaje.upper()
        
    elif LOGIC_TYPE == "REVERSE":
        # Lógica B: Invertir el texto
        data["mensaje"] = mensaje[::-1]
        
    elif LOGIC_TYPE == "COUNTER":
        # Lógica C: Sumar matemáticas
        data["contador"] = contador + 100
        
    elif LOGIC_TYPE == "PREFIX":
        # Lógica D: Agregar prefijo
        data["mensaje"] = f"KUBERNETES DICE: {mensaje}"
        
    # Siempre firmamos que pasamos por aquí
    data["camino"].append(f"{MY_NAME}({LOGIC_TYPE})")
    return data

# --- ENDPOINTS ---

@app.route('/start', methods=['GET'])
def start():
    # Solo el primer nodo debería usar esto para iniciar la cadena
    initial_data = {
        "mensaje": "hola evaluador",
        "contador": 0,
        "camino": []
    }
    # Nos procesamos a nosotros mismos primero
    processed_data = procesar_datos(initial_data)
    
    # Enviamos al siguiente en un hilo aparte
    def enviar():
        if NEXT_SERVICE:
            try:
                requests.post(f"{NEXT_SERVICE}/process", json=processed_data)
            except Exception as e:
                print(f"Error enviando al siguiente: {e}")
    
    threading.Thread(target=enviar).start()
    return jsonify({"status": "Iniciado", "data_inicial": processed_data})

@app.route('/process', methods=['POST'])
def receive():
    data = request.json
    
    # 1. Ejecutamos la lógica específica de este nodo
    data = procesar_datos(data)
    
    # 2. Verificamos si somos el último
    if IS_LAST == "yes":
        print(f"✅ FINAL DEL PROCESO. Resultado: {data}")
        return jsonify({"status": "finished", "final_data": data})
    
    # 3. Si no somos el último, pasamos al siguiente
    if NEXT_SERVICE:
        print(f"--> Pasando a {NEXT_SERVICE}")
        try:
            requests.post(f"{NEXT_SERVICE}/process", json=data)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
            
    return jsonify({"status": "passed"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)