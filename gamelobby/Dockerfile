FROM python:3.12-slim

WORKDIR /app
COPY . /app

RUN pip install flask flask-socketio eventlet

EXPOSE 80
CMD ["python", "app.py"]
