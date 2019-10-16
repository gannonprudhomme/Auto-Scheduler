from .base import *

SECRET_KEY = open("/run/secrets/SECRET_DJANGO_KEY").read()

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "dbautoscheduler",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "db",
    }
}