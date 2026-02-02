from flask import Flask, render_template_string, request, redirect
import requests
import os

app = Flask(__name__)

# Comunicación: HTTP Síncrona hacia el Backend
BACKEND_URL = os.getenv("BACKEND_URL", "http://backend-service:5000")

# HTML con TODOS los elementos solicitados (Combobox, Radio, Checkbox, etc)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Restaurante K8s</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
<div class="container mt-5">
    <h1 class="text-center mb-4">🍽️ Comandas Kubernetes</h1>
    
    <div class="row">
        <div class="col-md-5">
            <div class="card p-4 shadow-sm">
                <h4>Nuevo Pedido</h4>
                <form action="/add" method="POST">
                    
                    <div class="mb-3">
                        <label>Nombre del Cliente:</label>
                        <input type="text" name="cliente" class="form-control" required>
                    </div>

                    <div class="mb-3">
                        <label>Plato Principal:</label>
                        <select name="plato" class="form-select">
                            <option value="Hamburguesa">Hamburguesa</option>
                            <option value="Pizza">Pizza</option>
                            <option value="Ensalada">Ensalada</option>
                            <option value="Tacos">Tacos</option>
                        </select>
                    </div>

                    <div class="mb-3">
                        <label>Nivel de Picante:</label><br>
                        <input type="radio" name="picante" value="Bajo" checked> Bajo
                        <input type="radio" name="picante" value="Medio"> Medio
                        <input type="radio" name="picante" value="Alto"> Alto
                    </div>

                    <div class="mb-3">
                        <label>Extras:</label><br>
                        <input type="checkbox" name="extras" value="Queso"> Queso Extra<br>
                        <input type="checkbox" name="extras" value="Bacon"> Bacon<br>
                        <input type="checkbox" name="extras" value="Papas"> Papas Fritas
                    </div>

                    <div class="mb-3">
                        <label>Notas Especiales:</label>
                        <textarea name="notas" class="form-control" rows="2"></textarea>
                    </div>

                    <button type="submit" class="btn btn-primary w-100">Enviar a Cocina</button>
                </form>
            </div>
        </div>

        <div class="col-md-7">
            <h4>Pedidos en curso</h4>
            <div class="list-group">
                {% for order in orders %}
                <div class="list-group-item d-flex justify-content-between align-items-center">
                    <div>
                        <strong>{{ order.cliente }}</strong> - {{ order.plato }} 
                        <span class="badge bg-secondary">{{ order.status }}</span>
                        <br>
                        <small class="text-muted">Picante: {{ order.picante }} | Extras: {{ order.extras }}</small>
                    </div>
                    <div>
                         <form action="/delete/{{ order._id }}" method="POST" style="display:inline;">
                            <button type="submit" class="btn btn-danger btn-sm">X</button>
                        </form>
                    </div>
                </div>
                {% endfor %}
            </div>
            <br>
            <a href="/" class="btn btn-outline-secondary btn-sm">Actualizar Lista</a>
        </div>
    </div>
</div>
</body>
</html>
"""

@app.route('/')
def index():
    # READ: Pedimos la lista al Backend
    try:
        resp = requests.get(f"{BACKEND_URL}/orders")
        orders = resp.json()
    except:
        orders = []
    return render_template_string(HTML_TEMPLATE, orders=orders)

@app.route('/add', methods=['POST'])
def add_order():
    # Recogemos todos los campos del HTML
    new_order = {
        "cliente": request.form.get('cliente'),
        "plato": request.form.get('plato'),
        "picante": request.form.get('picante'),
        "extras": request.form.getlist('extras'), # Para checkboxes múltiples
        "notas": request.form.get('notas')
    }
    # CREATE: Enviamos al Backend
    requests.post(f"{BACKEND_URL}/orders", json=new_order)
    return redirect('/')

@app.route('/delete/<id>', methods=['POST'])
def delete_order(id):
    # DELETE: Enviamos orden de borrado al Backend
    requests.delete(f"{BACKEND_URL}/orders/{id}")
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)