FROM python:3.9-slim

WORKDIR /app

# Instala todo lo que podrías necesitar de una vez
RUN pip install flask requests pymongo redis

COPY . .

# Ejecuta tu script (asegúrate que se llame app.py)
CMD ["python", "app.py"]