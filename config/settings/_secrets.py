import environ

env = environ.Env()

SECRET_KEY = env('DJANGO_SECRET_KEY', default='secret_key').strip()
POSTGRES_DB = env('POSTGRES_DB', default='').strip()
POSTGRES_USER = env('POSTGRES_USER', default='').strip()
POSTGRES_PASSWORD = env('POSTGRES_PASSWORD', default='').strip()
POSTGRES_SUPERUSER = env('POSTGRES_SUPERUSER', default='').strip()
POSTGRES_SUPERUSER_PASSWORD = env('POSTGRES_SUPERUSER_PASSWORD', default='').strip()

CARTO_API_KEY = env('CARTO_API_KEY', default='').strip()
