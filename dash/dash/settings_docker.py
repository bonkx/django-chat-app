from .settings import *

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.environ.get("DB_NAME", "django_chat"),
        "HOST": os.environ.get("DB_HOST", "localhost"),
        "USER": os.environ.get("DB_USER", "postgres"),
        "PASSWORD": os.environ.get("DB_PASS", "postgres"),
        "PORT": os.environ.get("DB_PORT", "5432"),
    }
}