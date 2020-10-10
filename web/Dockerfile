FROM ubuntu:latest

RUN apt update -y;  apt upgrade -y
RUN apt install libpcre3 libpcre3-dev libpq-dev python-dev gcc -y
RUN apt install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt install python3.8 python3-pip  -y
RUN apt autoremove
ENV APP /app
RUN mkdir $APP
WORKDIR $APP
EXPOSE 9090
COPY requirements.txt .
RUN pip3 install -r requirements.txt
RUN pip3 install uwsgi
COPY . .
CMD [ "uwsgi", "--ini", "dev.ini" ]
