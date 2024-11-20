# Base python package
FROM python:3.12-slim

# Working directory
WORKDIR /app

# set flask to debug mode
ENV FLASK_DEBUG=1

# Copy the dependencies
COPY requirements.txt requirements.txt

# Install the dependencies
RUN pip install -r requirements.txt

# Executable commands
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=5000", "--reload"]
