FROM python:3

ENV APP /app 

RUN mkdir $APP
WORKDIR $APP 

EXPOSE 8080
COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD [ "uwsgi", "--ini", "app.ini" ]

