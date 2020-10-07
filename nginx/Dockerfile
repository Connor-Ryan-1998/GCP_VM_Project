FROM nginx:latest

EXPOSE 80

#Remove default
RUN rm /etc/nginx/conf.d/default.conf

#copy over new config
COPY nginx.conf /etc/nginx/conf.d


