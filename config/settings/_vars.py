from config.settings.base import env, os, ROOT_DIR

DEBUG = env('DEBUG', default=False)
DEBUG_LEVEL = env('DEBUG_LEVEL', default='ERROR').strip()

POSTGRES_HOST = env('POSTGRES_HOST', default='').strip()
POSTGRES_PORT = env('POSTGRES_PORT', default='')