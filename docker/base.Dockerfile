############
# Base Image
############
FROM python:3.11.3-slim AS base

RUN apt-get update && apt-get -y install libpq-dev gcc
RUN mkdir    /var/app
WORKDIR    /var/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /var/app/requirements.txt
COPY test-requirements.txt /var/app/test-requirements.txt

RUN pip3 install --no-cache-dir -r /var/app/test-requirements.txt


