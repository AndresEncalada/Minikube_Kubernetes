from flask import Flask, request, jsonify
from pymongo import MongoClient
import redis
import os
from bson.objectid import ObjectId

app = Flask(__name__)

# CONFIGURACIÓN DE CONEXIONES (Variables de entorno de K8s)
# Comunicación: TCP interna hacia MongoDB
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo-service:27017/")
client = MongoClient(MONGO_URI)
db = client.restaurant_db
orders = db.orders

# Comunicación: TCP interna hacia Redis (Cola)
REDIS_HOST = os.getenv("REDIS_HOST", "redis-service")
q = redis.Redis(host=REDIS_HOST, port=6379, db=0)

# --- CRUD: CREATE (POST) ---
@app.route('/orders', methods=['POST'])
def create_order():
    data = request.json
    # Guardamos en Mongo con estado "Pendiente"
    data['status'] = 'Pendiente'
    result = orders.insert_one(data)
    order_id = str(result.inserted_id)
    
    # Comunicación ASÍNCRONA: Enviamos el ID a la cola de Redis
    # El usuario no espera a que se cocine, solo recibe "Recibido"
    q.rpush('kitchen_queue', order_id)
    
    return jsonify({"id": order_id, "message": "Pedido enviado a cocina"}), 201

# --- CRUD: READ (GET) ---
@app.route('/orders', methods=['GET'])
def get_orders():
    all_orders = []
    for doc in orders.find():
        doc['_id'] = str(doc['_id'])
        all_orders.append(doc)
    return jsonify(all_orders)

# --- CRUD: UPDATE (PUT) ---
@app.route('/orders/<id>', methods=['PUT'])
def update_order(id):
    data = request.json
    orders.update_one({'_id': ObjectId(id)}, {'$set': data})
    return jsonify({"message": "Pedido actualizado"})

# --- CRUD: DELETE (DELETE) ---
@app.route('/orders/<id>', methods=['DELETE'])
def delete_order(id):
    orders.delete_one({'_id': ObjectId(id)})
    return jsonify({"message": "Pedido eliminado"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)