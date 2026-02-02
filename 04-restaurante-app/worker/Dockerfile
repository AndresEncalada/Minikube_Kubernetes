FROM python:3.9-slim
WORKDIR /app
# Usamos '-u' en python para ver los logs en tiempo real en Kubernetes
RUN pip install pymongo redis
COPY . .
CMD ["python", "-u", "worker.py"]