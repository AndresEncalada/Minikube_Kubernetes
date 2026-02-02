FROM python:3.9-slim
WORKDIR /app
RUN pip install flask pymongo redis
COPY . .
CMD ["python", "app.py"]