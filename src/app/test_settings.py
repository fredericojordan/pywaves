from .settings import *


DJANGO_DEBUG = True
ENVIRONMENT = "test"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "test",
        "HOST": "127.0.0.1",
        "PORT": 5432,
        "USER": "postgres",
        "PASSWORD": "postgres",
    }
}

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

PASSWORD_RESET_CONFIRM_PATH = "accouts/reset_password"
