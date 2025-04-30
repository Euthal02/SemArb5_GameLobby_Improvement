# Base python package
FROM python:3.12-slim

# Working directory
WORKDIR /app

# add files
ADD . /app

# Install requirements 
RUN pip install -r requirements.txt

# Install Gunicorn 
RUN pip install gunicorn==21.2

# for flask web server
EXPOSE 80

# This is the runtime command for the container
CMD [ "gunicorn", "--worker-class", "eventlet", "--bind", "0.0.0.0:80", "wsgi:app" ]
