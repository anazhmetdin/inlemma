FROM ubuntu:18.04
COPY . /app
WORKDIR /app

RUN apt update -y
RUN apt install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa -y
RUN apt update -y

RUN apt install python3.9 -y

RUN apt install python3.9-venv -y
RUN python3.9 -m ensurepip --upgrade
RUN python3.9 -m pip install --upgrade pip

RUN apt install -y python3.9-dev libpq-dev
RUN apt install -y gfortran libopenblas-dev liblapack-dev libatlas-base-dev
RUN pip3.9 install --upgrade setuptools
RUN apt install -y g++

RUN pip3.9 install -r requirements.txt

RUN apt install -y redis-server
RUN apt install -y systemd