from bookstoreapi.settings.base import *

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": "db.sqlite3"}}
