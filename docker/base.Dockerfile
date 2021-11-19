############
# Base Image
############
FROM python:3.6-slim AS base

RUN mkdir    /var/app
WORKDIR    /var/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /var/app/requirements.txt
COPY test-requirements.txt /var/app/test-requirements.txt

RUN pip install --no-cache-dir -r /var/app/test-requirements.txt


