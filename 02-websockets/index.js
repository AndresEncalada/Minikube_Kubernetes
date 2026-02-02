const app = require('express')();
const http = require('http').createServer(app);
const io = require('socket.io')(http);
const os = require('os');

app.get('/', (req, res) => {
  res.sendFile(__dirname + '/index.html');
});

io.on('connection', (socket) => {
  console.log('Usuario conectado');
  // Enviamos el nombre del POD para probar que la conexión no salta
  socket.emit('mensaje', `Conectado al servidor: ${os.hostname()}`);
});

http.listen(3000, () => {
  console.log('Escuchando en *:3000');
});