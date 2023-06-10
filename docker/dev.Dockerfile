#################
# BookStore development Image
#################
FROM base

ENV DJANGO_SETTINGS_MODULE bookstoreapi.settings.dev

COPY       bookstoreapi /var/app/bookstoreapi

COPY       pytest.ini /var/app/pytest.ini
COPY       manage.py /var/app/manage.py
COPY       quick_test_seeding.py /var/app/quick_test_seeding.py
COPY       Makefile /var/app/Makefile

COPY       scripts/run_local.sh /var/app/scripts/run_local.sh
COPY       scripts/test_local_backend.sh /var/app/scripts/test_local_backend.sh

RUN        chmod +x /var/app/scripts/run_local.sh && chmod +x /var/app/scripts/test_local_backend.sh
EXPOSE     8001
CMD        ["make run_local"]