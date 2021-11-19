from bookstoreapi.settings.base import *

SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY", "alq7#8r33k!cv47r8pelqldnkl46v!b4-sfwvdo$x(=p%1read"
)

local_test_db = {"ENGINE": "django.db.backends.sqlite3", "NAME": "test_db"}

ci_db = {
    "ENGINE": "django.db.backends.postgresql_psycopg2",
    "NAME": os.getenv("CI_DATABASE_NAME"),
    "USER": os.getenv("CI_DATABASE_USER"),
    "HOST": os.getenv("CI_DATABASE_HOST"),
}


DATABASES = {"default": ci_db if os.getenv("CI_DATABASE_NAME") else local_test_db}
