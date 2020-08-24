SELECT 'CREATE DATABASE stations OWNER stationsuser ENCODING ''UTF-8'''
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'stations')\gexec
