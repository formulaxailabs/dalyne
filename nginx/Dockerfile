FROM nginx:1.19.4-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx-template.template /etc/nginx/conf.d/nginx-template.template
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENV DJANGOAPP="http://localhost:8000/"
RUN chmod 0777 /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
