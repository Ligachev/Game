FROM python:3.11

WORKDIR /app

ADD requirements.txt /app/
RUN pip install -r requirements.txt

ADD config-docker.ini /app/config.ini
ADD mygame /app/mygame
