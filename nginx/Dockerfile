FROM nginx:latest

EXPOSE 80

#Remove default
RUN rm /etc/nginx/conf.d/default.conf

#copy over new config
COPY app.conf/app.conf /etc/nginx/conf.d


