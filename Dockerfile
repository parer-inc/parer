FROM python:3.8-slim-buster

WORKDIR /usr/src/app
ENV PYTHONUNBUFFERED = 1
COPY requirements.txt requirements.txt

RUN apt-get -y update && \
	apt-get -y install \
	gcc \
	default-libmysqlclient-dev \
	python3-dev
RUN python3 -m pip install -r requirements.txt

COPY . .
