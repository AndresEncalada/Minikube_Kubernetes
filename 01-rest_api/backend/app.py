from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/api/data')
def get_data():
    # Simulamos datos de una DB
    return jsonify({
        "message": "Hola desde el Backend Python",
        "pod_name": os.getenv("HOSTNAME", "unknown")
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)