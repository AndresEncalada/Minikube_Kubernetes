import os
import threading
import time
import requests  # Para llamar a otros microservicios
import redis     # Para conectar a Redis
from flask import Flask, request, jsonify, render_template_string
from pymongo import MongoClient # Para conectar a MongoDB

app = Flask(__name__)

# ==========================================
# 1. CONFIGURACIÓN (VARIABLES DE ENTORNO)
# ==========================================
# El segundo valor es el "por defecto" si falla K8s.
MY_NAME = os.getenv("MY_NAME", "Servicio-Python")
TARGET_URL = os.getenv("TARGET_URL", "http://otro-servicio:5000")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo-service:27017/")
REDIS_HOST = os.getenv("REDIS_HOST", "redis-service")

# Conexión Segura a DB 
try:
    mongo_client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
    db = mongo_client.mi_base_de_datos
    collection = db.mi_coleccion
except:
    print("⚠️ ADVERTENCIA: No hay MongoDB conectado")

try:
    cache = redis.Redis(host=REDIS_HOST, port=6379, db=0)
except:
    print("⚠️ ADVERTENCIA: No hay Redis conectado")

# ==========================================
# 2. RUTAS BÁSICAS (GET)
# ==========================================
@app.route('/')
def home():
    # Retorna HTML simple 
    return f"<h1>Hola desde {MY_NAME}</h1><p>Todo funcionando.</p>"

@app.route('/health')
def health():
    # Retorna JSON 
    return jsonify({"status": "ok", "service": MY_NAME})

# ==========================================
# 3. RECIBIR DATOS (POST - JSON y FORM)
# ==========================================
@app.route('/procesar', methods=['POST'])
def procesar():
    #  JSON (API REST)
    if request.is_json:
        data = request.json
        mensaje = data.get("mensaje", "")
    
    # Formulario HTML
    else:
        mensaje = request.form.get("input_html", "")

    # Lógica simple (Ejemplos de manipulación)
    respuesta = {
        "original": mensaje,
        "mayusculas": mensaje.upper(),
        "invertido": mensaje[::-1],
        "longitud": len(mensaje)
    }
    return jsonify(respuesta)

# ==========================================
# 4. LLAMAR A OTRO MICROSERVICIO (CLIENTE)
# ==========================================
@app.route('/llamar-siguiente')
def llamar_siguiente():
    try:
        # Enviamos datos al siguiente servicio
        payload = {"origen": MY_NAME, "mensaje": "Hola vecino"}
        response = requests.post(f"{TARGET_URL}/procesar", json=payload, timeout=5)
        
        return jsonify({
            "status": "exito", 
            "respuesta_del_vecino": response.json()
        })
    except Exception as e:
        return jsonify({"error": f"El vecino no responde: {str(e)}"}), 500

# ==========================================
# 5. BASE DE DATOS (MONGO DB - CRUD)
# ==========================================
@app.route('/guardar', methods=['POST'])
def guardar_mongo():
    datos = request.json
    # Insertar
    collection.insert_one(datos)
    return jsonify({"status": "guardado"})

@app.route('/leer', methods=['GET'])
def leer_mongo():
    lista = []
    # Leer todo (convertimos _id a string porque o si no falla)
    for doc in collection.find():
        doc['_id'] = str(doc['_id'])
        lista.append(doc)
    return jsonify(lista)

# ==========================================
# 6. COLA DE MENSAJES (REDIS)
# ==========================================
@app.route('/encolar', methods=['POST'])
def encolar_tarea():
    msg = request.json.get('tarea', 'nada')
    # Empujar a la lista 'mis_tareas'
    cache.rpush('mis_tareas', msg)
    return jsonify({"status": "encolado"})

# ==========================================
# 7. PROCESO EN SEGUNDO PLANO (WORKER)
# ==========================================
# "Procesar sin bloquear" o "Simular trabajo pesado"
def tarea_larga(nombre):
    print(f"--> Iniciando tarea: {nombre}")
    time.sleep(5) # Simula espera de 5 segundos
    print(f"--> Tarea {nombre} terminada")

@app.route('/background')
def background():
    # Lanza el hilo y retorna inmediatamente al usuario
    hilo = threading.Thread(target=tarea_larga, args=("Proceso 1",))
    hilo.start()
    return jsonify({"message": "Tarea iniciada en background (mira los logs)"})

# ==========================================
# 8. SERVIDOR WEB
# ==========================================
if __name__ == '__main__':
    # host='0.0.0.0' ES OBLIGATORIO en Docker/K8s
    app.run(host='0.0.0.0', port=5000, debug=True)