#!/bin/sh
envsubst '${DJANGOAPP}' < /etc/nginx/conf.d/nginx-template.template > /etc/nginx/conf.d/nginx.conf
cat /etc/nginx/conf.d/nginx.conf
nginx -g 'daemon off;'
