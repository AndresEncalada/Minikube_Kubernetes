FROM node:14-alpine
WORKDIR /app
COPY . .
RUN npm install express socket.io
CMD ["node", "index.js"]