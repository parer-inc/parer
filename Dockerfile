FROM python:3.8-slim-buster

WORKDIR /usr/src/app
ENV PYTHONUNBUFFERED = 1
RUN apt-get -y update
RUN apt-get -y install gcc
RUN apt-get -y install default-libmysqlclient-dev
RUN apt-get -y install python3-dev
COPY requirements.txt requirements.txt
RUN python3 -m pip install -r requirements.txt

COPY . .
