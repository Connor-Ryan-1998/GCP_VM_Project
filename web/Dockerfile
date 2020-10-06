# FROM python:3.8

# ENV APP /app 

# RUN mkdir $APP
# WORKDIR $APP 

# EXPOSE 8080
# COPY requirements.txt .

# RUN pip install -r requirements.txt

# COPY . .

# CMD [ "uwsgi", "--ini", "dev.ini" ]

FROM ubuntu:latest

RUN apt update -y;  apt upgrade -y
RUN apt install software-properties-common -y
RUN apt install libpcre3-dev -y
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt install python3.8 python3-pip  -y
ENV APP /app
RUN mkdir $APP
WORKDIR $APP
EXPOSE 8080
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .
CMD [ "uwsgi", "--ini", "dev.ini" ]
