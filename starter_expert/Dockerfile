FROM python:3.11

RUN apt-get update -y
RUN apt-get upgrade -y

WORKDIR /app

RUN pip install --upgrade pip
COPY ./requirements.txt ./
RUN pip install -r requirements.txt
COPY ./proj ./src

