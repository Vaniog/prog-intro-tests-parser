FROM python:3.10.12
SHELL ["/bin/bash", "-c"]
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . /app
WORKDIR /app 
RUN pip install -r requirements.txt
CMD ["flask", "db", "upgrade"]
CMD ["gunicorn","-b","0.0.0.0:8000","app:create_app()"]