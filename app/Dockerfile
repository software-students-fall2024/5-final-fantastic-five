# Dockerfile for Flask API
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 3000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:3000", "app:APP"]

