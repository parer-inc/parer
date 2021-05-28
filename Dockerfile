FROM python:3.8

WORKDIR /usr/src/app
ENV PYTHONUNBUFFERED = 1

RUN apt-get update \
  && apt install -y default-libmysqlclient-dev  python3-dev

COPY requirements.txt requirements.txt
RUN python3 -m pip install -r requirements.txt

COPY . .
