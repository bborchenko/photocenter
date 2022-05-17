FROM nginxinc/nginx-unprivileged:1-alpine
COPY ./default.conf /etc/nginx/conf.d/default.conf
COPY ./uwsgi_params /etc/nginx/uwsgi_params

USER root
RUN mkdir /static
RUN chmod 755 /static
RUN chown -R nginx:nginx /etc/nginx
USER nginx

