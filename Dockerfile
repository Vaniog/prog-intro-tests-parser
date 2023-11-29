FROM python:3.10.12
SHELL ["/bin/bash", "-c"]
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . /app
WORKDIR /app

CMD ["/bin/bash","-c","./start.sh"]