FROM nginx:latest

EXPOSE 80

#Remove default
RUN rm /etc/nginx/conf.d/default.conf

COPY sites-enabled/app.conf /etc/nginx/conf.d

