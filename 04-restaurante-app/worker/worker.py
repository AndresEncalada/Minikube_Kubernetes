import redis
import time
import os
from pymongo import MongoClient
from bson.objectid import ObjectId

# Conexiones iguales al backend
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo-service:27017/")
client = MongoClient(MONGO_URI)
db = client.restaurant_db
orders = db.orders

REDIS_HOST = os.getenv("REDIS_HOST", "redis-service")
q = redis.Redis(host=REDIS_HOST, port=6379, db=0)

print("Cocinero listo para recibir comandas...")

while True:
    # 1. Esperar mensaje en la cola 'kitchen_queue' (Blocking Pop)
    # Esto es comunicación por SOCKETS TCP raw hacia Redis
    task = q.blpop('kitchen_queue', timeout=0)
    
    if task:
        order_id = task[1].decode('utf-8')
        print(f"Cocinando pedido: {order_id}")
        
        # 2. Actualizar estado a "Cocinando"
        orders.update_one({'_id': ObjectId(order_id)}, {'$set': {'status': 'Cocinando...'}})
        
        # 3. Simular tiempo de cocina (10 segundos)
        time.sleep(10)
        
        # 4. Actualizar estado a "Listo"
        orders.update_one({'_id': ObjectId(order_id)}, {'$set': {'status': 'Listo para servir'}})
        print(f"Pedido {order_id} terminado.")