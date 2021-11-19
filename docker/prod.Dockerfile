#################
# BookStore production Image
#################
FROM python:3.6-slim AS base

RUN mkdir    /var/app
WORKDIR    /var/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV DJANGO_SETTINGS_MODULE bookstoreapi.settings.prod

COPY requirements.txt /var/app/requirements.txt
RUN pip install --no-cache-dir -r /var/app/requirements.txt

COPY       . /var/app/bookstoreapi

COPY       scripts/run_prod.sh /var/app/run_prod.sh
COPY       scripts/test_local_backend.sh /var/app/test_local_backend.sh
RUN        chmod +x run_prod.sh

EXPOSE     8001
CMD        ["/var/app/run_prod.sh"]