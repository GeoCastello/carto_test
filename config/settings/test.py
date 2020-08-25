from .base import *

DEBUG = True
TEST_RUNNER = "django.test.runner.DiscoverRunner"

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'docker',
        'USER': POSTGRES_SUPERUSER,
        'PASSWORD': POSTGRES_SUPERUSER_PASSWORD,
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
