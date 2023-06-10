#################
# BookStore production Image
#################
FROM base

ENV DJANGO_SETTINGS_MODULE bookstoreapi.settings.prod

COPY requirements.txt /var/app/requirements.txt
RUN pip install --no-cache-dir -r /var/app/requirements.txt

COPY       bookstoreapi /var/app/bookstoreapi

COPY       pytest.ini /var/app/pytest.ini
COPY       manage.py /var/app/manage.py
COPY       quick_test_seeding.py /var/app/quick_test_seeding.py
COPY       Makefile /var/app/Makefile

COPY       scripts/run_prod.sh /var/app/scripts/run_prod.sh
RUN        chmod +x /var/app/scripts/run_prod.sh

EXPOSE     8001
CMD        ["make run_prod"]