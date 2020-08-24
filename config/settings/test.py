from .base import *

DEBUG = True
TEST_RUNNER = "django.test.runner.DiscoverRunner"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'docker',
        'USER': 'docker',
        'PASSWORD': 'docker',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
