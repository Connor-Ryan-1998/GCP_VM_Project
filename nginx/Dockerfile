FROM nginx:latest

EXPOSE 80

#Remove default
RUN rm /etc/nginx/conf.d/default.conf
RUN rm /etc/nginx/sites-enabled/default

COPY sites-enabled/app.conf /etc/nginx/conf.d
COPY sites-enabled/flask_project /etc/nginx/sites-enabled

