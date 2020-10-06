FROM python:3.8

ENV APP /app 

RUN mkdir $APP
WORKDIR $APP 

EXPOSE 9090
COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD [ "uwsgi", "--ini", "dev.ini" ]

