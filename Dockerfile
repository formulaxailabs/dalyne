FROM python:3.9.4-slim-buster
MAINTAINER Abhisek singh <abhisek.singh@formulaxai.com>
COPY ./entrypoint.sh /entrypoint.sh
WORKDIR /dalyne
COPY ./requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /requirements.txt
COPY ./dalyne /dalyne
ENTRYPOINT ["/entrypoint.sh"]
