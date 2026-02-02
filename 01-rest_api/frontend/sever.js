const express = require('express');
const http = require('http');
const app = express();

// Leemos la URL del backend desde el ConfigMap de K8s
const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:5000';

app.get('/', (req, res) => {
    http.get(`${BACKEND_URL}/api/data`, (resp) => {
        let data = '';
        resp.on('data', (chunk) => { data += chunk; });
        resp.on('end', () => {
            res.send(`<h1>Frontend</h1><p>Respuesta del Backend: ${data}</p>`);
        });
    }).on("error", (err) => {
        res.send("Error conectando al backend: " + err.message);
    });
});

app.listen(3000, () => console.log('Frontend en puerto 3000'));