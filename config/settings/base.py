"""
Base settings to build other settings files upon.
"""
import sys
import environ
import os

env = environ.Env()

ROOT_DIR = environ.Path(__file__) - 3
APPS_DIR = ROOT_DIR.path('carto_test')

READ_DOT_ENV_FILE = env.bool('DJANGO_READ_DOT_ENV_FILE', default=False)
CARTO_TEST_ENV = env('CARTO_TEST_ENV', default='local')

if READ_DOT_ENV_FILE:
    print(f'\U0001F40D *** Loading environment: {CARTO_TEST_ENV} *** \U0001F40D')
    env_files = ['.vars', '.secrets']
    env_files_paths = [str(ROOT_DIR.path(f'.envs/{CARTO_TEST_ENV}/{env_file}')) for env_file in env_files]
    for env_file_path in env_files_paths:
        if os.path.isfile(env_file_path):
            env.read_env(env_file_path)
        else:
            print(f'*** \U0001F525 Warning: missing env file: {env_file_path}\n', file=sys.stderr)

from ._vars import *
from ._secrets import *

TIME_ZONE = 'Europe/Madrid'
LANGUAGE_CODE = 'es-es'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = (
    ('es', 'Spanish'),
    ('en', 'English'),
)

LOCALE_PATHS = (
    os.path.join(APPS_DIR, 'locale'),
)

# URLS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = 'config.urls'
# https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'config.wsgi.application'

# APPS
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'rest_framework',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.gis',
]
THIRD_PARTY_APPS = []
LOCAL_APPS = [
    'carto_test.apps.air_quality',
]
# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIDDLEWARE
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

STATIC_URL = '/static/'

LANGUAGE_DEFAULT = {
    'language_code': 'en',
    'language_country': 'EN',
    'language_name': 'English'
}
LANGUAGES_AVAILABLE = ['es', 'en']
