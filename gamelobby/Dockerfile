FROM python:3.12-slim

WORKDIR /app
COPY . /app

# Install requirements 
RUN pip install -r requirements.txt

EXPOSE 80
CMD ["python3", "app.py"]
